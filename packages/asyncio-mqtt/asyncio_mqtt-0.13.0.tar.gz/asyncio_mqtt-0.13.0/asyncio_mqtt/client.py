# SPDX-License-Identifier: BSD-3-Clause
import asyncio
import functools
import logging
import socket
import ssl
import sys
from contextlib import contextmanager
from enum import IntEnum
from types import TracebackType
from typing import (
    Any,
    AsyncContextManager,
    AsyncGenerator,
    AsyncIterator,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

if sys.version_info >= (3, 7):
    from contextlib import asynccontextmanager
else:
    from async_generator import asynccontextmanager as _asynccontextmanager

    _P = ParamSpec("_P")
    _T = TypeVar("_T")

    def asynccontextmanager(
        func: Callable[_P, AsyncIterator[_T]]
    ) -> Callable[_P, AsyncContextManager[_T]]:
        return _asynccontextmanager(func)


import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties

from .error import MqttCodeError, MqttConnectError, MqttError
from .types import PayloadType, T

MQTT_LOGGER = logging.getLogger("mqtt")
MQTT_LOGGER.setLevel(logging.WARNING)

_PahoSocket = Union[socket.socket, ssl.SSLSocket, mqtt.WebsocketWrapper, Any]

WebSocketHeaders = Union[
    Dict[str, Any],
    Callable[[Dict[str, Any]], Dict[str, Any]],
]


class ProtocolVersion(IntEnum):
    """
    A mapping of Paho MQTT protocol version constants to an Enum for use in type hints.
    """

    V31 = mqtt.MQTTv31
    V311 = mqtt.MQTTv311
    V5 = mqtt.MQTTv5


# TODO: This should be a (frozen) dataclass (from Python 3.7)
# when we drop Python 3.6 support
class Will:
    def __init__(
        self,
        topic: str,
        payload: Optional[PayloadType] = None,
        qos: int = 0,
        retain: bool = False,
        properties: Optional[mqtt.Properties] = None,
    ):
        self.topic = topic
        self.payload = payload
        self.qos = qos
        self.retain = retain
        self.properties = properties


# TLS set parameter class
class TLSParameters:
    def __init__(
        self,
        *,
        ca_certs: Optional[str] = None,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
        cert_reqs: Optional[ssl.VerifyMode] = None,
        tls_version: Optional[Any] = None,
        ciphers: Optional[str] = None,
        keyfile_password: Optional[str] = None,
    ):
        self.ca_certs = ca_certs
        self.certfile = certfile
        self.keyfile = keyfile
        self.cert_reqs = cert_reqs
        self.tls_version = tls_version
        self.ciphers = ciphers
        self.keyfile_password = keyfile_password


# Proxy parameters class
class ProxySettings:
    def __init__(
        self,
        *,
        proxy_type: int,
        proxy_addr: str,
        proxy_rdns: Optional[bool] = True,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
    ):
        self.proxy_args = {
            "proxy_type": proxy_type,
            "proxy_addr": proxy_addr,
            "proxy_rdns": proxy_rdns,
            "proxy_username": proxy_username,
            "proxy_password": proxy_password,
        }


# See the overloads of `socket.setsockopt` for details.
SocketOption = Union[
    Tuple[int, int, Union[int, bytes]],
    Tuple[int, int, None, int],
]

P = ParamSpec("P")

# TODO: Simplify the logic that surrounds `self._outgoing_calls_sem` with
# `nullcontext` when we support Python 3.10 (`nullcontext` becomes async-aware in
# 3.10). See: https://docs.python.org/3/library/contextlib.html#contextlib.nullcontext
def _outgoing_call(
    method: Callable[P, Coroutine[Any, Any, T]]
) -> Callable[P, Coroutine[Any, Any, T]]:
    @functools.wraps(method)
    async def decorated(*args: Any, **kwargs: Any) -> T:
        # `args[0]` is `self` from the methods of `Client`
        if not args[0]._outgoing_calls_sem:
            return await method(*args, **kwargs)

        async with args[0]._outgoing_calls_sem:
            return await method(*args, **kwargs)

    return decorated


class Client:
    def __init__(
        self,
        hostname: str,
        port: int = 1883,
        *,
        username: Optional[str] = None,
        password: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        client_id: Optional[str] = None,
        tls_context: Optional[ssl.SSLContext] = None,
        tls_params: Optional[TLSParameters] = None,
        proxy: Optional[ProxySettings] = None,
        protocol: Optional[ProtocolVersion] = None,
        will: Optional[Will] = None,
        clean_session: Optional[bool] = None,
        transport: str = "tcp",
        keepalive: int = 60,
        bind_address: str = "",
        bind_port: int = 0,
        clean_start: int = mqtt.MQTT_CLEAN_START_FIRST_ONLY,
        properties: Optional[Properties] = None,
        message_retry_set: int = 20,
        socket_options: Optional[Iterable[SocketOption]] = None,
        max_concurrent_outgoing_calls: Optional[int] = None,
        websocket_path: Optional[str] = None,
        websocket_headers: Optional[WebSocketHeaders] = None,
    ):
        self._hostname = hostname
        self._port = port
        self._keepalive = keepalive
        self._bind_address = bind_address
        self._bind_port = bind_port
        self._clean_start = clean_start
        self._properties = properties
        self._loop = asyncio.get_event_loop()
        self._connected: asyncio.Future[Union[int, mqtt.ReasonCodes]] = asyncio.Future()
        self._disconnected: asyncio.Future[
            Union[int, mqtt.ReasonCodes, None]
        ] = asyncio.Future()
        # Pending subscribe, unsubscribe, and publish calls
        self._pending_subscribes: Dict[
            int, asyncio.Future[Union[Tuple[int], List[mqtt.ReasonCodes]]]
        ] = {}
        self._pending_unsubscribes: Dict[int, asyncio.Event] = {}
        self._pending_publishes: Dict[int, asyncio.Event] = {}
        self._pending_calls_threshold: int = 10
        self._misc_task: Optional[asyncio.Task[None]] = None

        self._outgoing_calls_sem: Optional[asyncio.Semaphore]
        if max_concurrent_outgoing_calls is not None:
            self._outgoing_calls_sem = asyncio.Semaphore(max_concurrent_outgoing_calls)
        else:
            self._outgoing_calls_sem = None

        if protocol is None:
            protocol = ProtocolVersion.V311

        self._client: mqtt.Client = mqtt.Client(
            client_id=client_id,
            protocol=protocol,
            clean_session=clean_session,
            transport=transport,
            reconnect_on_failure=False,
        )
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_unsubscribe = self._on_unsubscribe
        self._client.on_message = None
        self._client.on_publish = self._on_publish
        # Callbacks for custom event loop
        self._client.on_socket_open = self._on_socket_open
        self._client.on_socket_close = self._on_socket_close
        self._client.on_socket_register_write = self._on_socket_register_write
        self._client.on_socket_unregister_write = self._on_socket_unregister_write

        if logger is None:
            logger = MQTT_LOGGER
        self._client.enable_logger(logger)

        if username is not None:
            self._client.username_pw_set(username=username, password=password)

        if tls_context is not None:
            self._client.tls_set_context(tls_context)

        if tls_params is not None:
            self._client.tls_set(
                ca_certs=tls_params.ca_certs,
                certfile=tls_params.certfile,
                keyfile=tls_params.keyfile,
                cert_reqs=tls_params.cert_reqs,
                tls_version=tls_params.tls_version,
                ciphers=tls_params.ciphers,
                keyfile_password=tls_params.keyfile_password,
            )

        if proxy is not None:
            self._client.proxy_set(**proxy.proxy_args)

        if websocket_path is not None:
            self._client.ws_set_options(path=websocket_path, headers=websocket_headers)

        if will is not None:
            self._client.will_set(
                will.topic, will.payload, will.qos, will.retain, will.properties
            )

        self._client.message_retry_set(message_retry_set)
        if socket_options is None:
            socket_options = ()
        self._socket_options: Tuple[SocketOption, ...] = tuple(socket_options)

    @property
    def id(self) -> str:
        """Return the client ID.

        Note that paho-mqtt stores the client ID as `bytes` internally.
        We assume that the client ID is a UTF8-encoded string and decode
        it first.
        """
        return cast(bytes, self._client._client_id).decode()  # type: ignore[attr-defined]

    @property
    def _pending_calls(self) -> Generator[int, None, None]:
        """
        Yield all message IDs with pending calls.
        """
        yield from self._pending_subscribes.keys()
        yield from self._pending_unsubscribes.keys()
        yield from self._pending_publishes.keys()

    async def connect(self, *, timeout: int = 10) -> None:
        try:
            # get_running_loop is preferred, but only available in python>=3.7
            try:
                loop = asyncio.get_running_loop()
            except AttributeError:
                loop = asyncio.get_event_loop()

            # [3] Run connect() within an executor thread, since it blocks on socket
            # connection for up to `keepalive` seconds: https://git.io/Jt5Yc
            await loop.run_in_executor(
                None,
                self._client.connect,
                self._hostname,
                self._port,
                self._keepalive,
                self._bind_address,
                self._bind_port,
                self._clean_start,
                self._properties,
            )
            client_socket = self._client.socket()
            _set_client_socket_defaults(client_socket, self._socket_options)
        # paho.mqtt.Client.connect may raise one of several exceptions.
        # We convert all of them to the common MqttError for user convenience.
        # See: https://github.com/eclipse/paho.mqtt.python/blob/v1.5.0/src/paho/mqtt/client.py#L1770
        except (socket.error, OSError, mqtt.WebsocketConnectionError) as error:
            raise MqttError(str(error))
        await self._wait_for(self._connected, timeout=timeout)

    async def disconnect(self, *, timeout: int = 10) -> None:
        rc = self._client.disconnect()
        # Early out on error
        if rc != mqtt.MQTT_ERR_SUCCESS:
            raise MqttCodeError(rc, "Could not disconnect")
        # Wait for acknowledgement
        await self._wait_for(self._disconnected, timeout=timeout)

    async def force_disconnect(self) -> None:
        if not self._disconnected.done():
            self._disconnected.set_result(None)

    @_outgoing_call
    async def subscribe(
        self,
        topic: Union[
            str,
            Tuple[str, mqtt.SubscribeOptions],
            List[Tuple[str, mqtt.SubscribeOptions]],
            List[Tuple[str, int]],
        ],
        qos: int = 0,
        options: Optional[mqtt.SubscribeOptions] = None,
        properties: Optional[Properties] = None,
        *args: Any,
        timeout: int = 10,
        **kwargs: Any,
    ) -> Union[Tuple[int], List[mqtt.ReasonCodes]]:
        result, mid = self._client.subscribe(
            topic, qos, options, properties, *args, **kwargs
        )
        # Early out on error
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise MqttCodeError(result, "Could not subscribe to topic")
        # Create future for when the on_subscribe callback is called
        cb_result: asyncio.Future[
            Union[Tuple[int], List[mqtt.ReasonCodes]]
        ] = asyncio.Future()
        with self._pending_call(mid, cb_result, self._pending_subscribes):
            # Wait for cb_result
            return await self._wait_for(cb_result, timeout=timeout)

    @_outgoing_call
    async def unsubscribe(
        self,
        topic: Union[str, List[str]],
        properties: Optional[Properties] = None,
        *args: Any,
        timeout: int = 10,
        **kwargs: Any,
    ) -> None:
        result, mid = self._client.unsubscribe(topic, properties, *args, **kwargs)
        # Early out on error
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise MqttCodeError(result, "Could not unsubscribe from topic")
        # Create event for when the on_unsubscribe callback is called
        confirmation = asyncio.Event()
        with self._pending_call(mid, confirmation, self._pending_unsubscribes):
            # Wait for confirmation
            await self._wait_for(confirmation.wait(), timeout=timeout)

    @_outgoing_call
    async def publish(
        self,
        topic: str,
        payload: PayloadType = None,
        qos: int = 0,
        retain: bool = False,
        properties: Optional[Properties] = None,
        *args: Any,
        timeout: int = 10,
        **kwargs: Any,
    ) -> None:
        info = self._client.publish(
            topic, payload, qos, retain, properties, *args, **kwargs
        )  # [2]
        # Early out on error
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise MqttCodeError(info.rc, "Could not publish message")
        # Early out on immediate success
        if info.is_published():
            return
        # Create event for when the on_publish callback is called
        confirmation = asyncio.Event()
        with self._pending_call(info.mid, confirmation, self._pending_publishes):
            # Wait for confirmation
            await self._wait_for(confirmation.wait(), timeout=timeout)

    @asynccontextmanager
    async def filtered_messages(
        self, topic_filter: str, *, queue_maxsize: int = 0
    ) -> AsyncIterator[AsyncGenerator[mqtt.MQTTMessage, None]]:
        """Return async generator of messages that match the given filter.

        Use queue_maxsize to restrict the queue size. If the queue is full,
        incoming messages will be discarded (and a warning is logged).
        If queue_maxsize is less than or equal to zero, the queue size is infinite.

        Example use:
            async with client.filtered_messages('floors/+/humidity') as messages:
                async for message in messages:
                    print(f'Humidity reading: {message.payload.decode()}')
        """
        cb, generator = self._cb_and_generator(
            log_context=f'topic_filter="{topic_filter}"', queue_maxsize=queue_maxsize
        )
        try:
            self._client.message_callback_add(topic_filter, cb)
            # Back to the caller (run whatever is inside the with statement)
            yield generator
        finally:
            # We are exitting the with statement. Remove the topic filter.
            self._client.message_callback_remove(topic_filter)

    @asynccontextmanager
    async def unfiltered_messages(
        self, *, queue_maxsize: int = 0
    ) -> AsyncIterator[AsyncGenerator[mqtt.MQTTMessage, None]]:
        """Return async generator of all messages that are not caught in filters."""
        # Early out
        if self._client.on_message is not None:
            # TODO: This restriction can easily be removed.
            raise RuntimeError(
                "Only a single unfiltered_messages generator can be used at a time."
            )
        cb, generator = self._cb_and_generator(
            log_context="unfiltered", queue_maxsize=queue_maxsize
        )
        try:
            self._client.on_message = cb
            # Back to the caller (run whatever is inside the with statement)
            yield generator
        finally:
            # We are exitting the with statement. Unset the callback.
            self._client.on_message = None

    def _cb_and_generator(
        self, *, log_context: str, queue_maxsize: int = 0
    ) -> Tuple[
        Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None],
        AsyncGenerator[mqtt.MQTTMessage, None],
    ]:
        # Queue to hold the incoming messages
        messages: asyncio.Queue[mqtt.MQTTMessage] = asyncio.Queue(maxsize=queue_maxsize)
        # Callback for the underlying API
        def _put_in_queue(
            client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
        ) -> None:
            try:
                messages.put_nowait(msg)
            except asyncio.QueueFull:
                MQTT_LOGGER.warning(
                    f"[{log_context}] Message queue is full. Discarding message."
                )

        # The generator that we give to the caller
        async def _message_generator() -> AsyncGenerator[mqtt.MQTTMessage, None]:
            # Forward all messages from the queue
            while True:
                # Wait until we either:
                #  1. Receive a message
                #  2. Disconnect from the broker
                get: asyncio.Task[mqtt.MQTTMessage] = self._loop.create_task(
                    messages.get()
                )
                try:
                    done, _ = await asyncio.wait(
                        (get, self._disconnected), return_when=asyncio.FIRST_COMPLETED
                    )
                except asyncio.CancelledError:
                    # If the asyncio.wait is cancelled, we must make sure
                    # to also cancel the underlying tasks.
                    get.cancel()
                    raise
                if get in done:
                    # We received a message. Return the result.
                    yield get.result()
                else:
                    # We got disconnected from the broker. Cancel the "get" task.
                    get.cancel()
                    # Stop the generator with the following exception
                    raise MqttError("Disconnected during message iteration")

        return _put_in_queue, _message_generator()

    async def _wait_for(
        self, fut: Awaitable[T], timeout: Optional[float], **kwargs: Any
    ) -> T:
        try:
            return await asyncio.wait_for(fut, timeout=timeout, **kwargs)
        except asyncio.TimeoutError:
            raise MqttError("Operation timed out")

    @contextmanager
    def _pending_call(
        self, mid: int, value: T, pending_dict: Dict[int, T]
    ) -> Iterator[None]:
        if mid in self._pending_calls:
            raise RuntimeError(
                f'There already exists a pending call for message ID "{mid}"'
            )
        pending_dict[mid] = value  # [1]
        try:
            # Log a warning if there is a concerning number of pending calls
            pending = len(list(self._pending_calls))
            if pending > self._pending_calls_threshold:
                MQTT_LOGGER.warning(f"There are {pending} pending publish calls.")
            # Back to the caller (run whatever is inside the with statement)
            yield
        finally:
            # The normal procedure is:
            #  * We add the item at [1]
            #  * A callback will remove the item
            #
            # However, if the callback doesn't get called (e.g., due to a
            # network error) we still need to remove the item from the dict.
            try:
                del pending_dict[mid]
            except KeyError:
                pass

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: Dict[str, int],
        rc: Union[int, mqtt.ReasonCodes],
        properties: Optional[mqtt.Properties] = None,
    ) -> None:
        # Return early if already connected. Sometimes, paho-mqtt calls _on_connect
        # multiple times. Maybe because we receive multiple CONNACK messages
        # from the server. In any case, we return early so that we don't set
        # self._connected twice (as it raises an asyncio.InvalidStateError).
        if self._connected.done():
            return

        if rc == mqtt.CONNACK_ACCEPTED:
            self._connected.set_result(rc)
        else:
            self._connected.set_exception(MqttConnectError(rc))

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        rc: Union[int, mqtt.ReasonCodes, None],
        properties: Optional[mqtt.Properties] = None,
    ) -> None:
        # Return early if the disconnect is already acknowledged.
        # Sometimes (e.g., due to timeouts), paho-mqtt calls _on_disconnect
        # twice. We return early to avoid setting self._disconnected twice
        # (as it raises an asyncio.InvalidStateError).
        if self._disconnected.done():
            return
        # Return early if we are not connected yet. This avoids calling
        # `_disconnected.set_exception` with an exception that will never
        # be retrieved (since `__aexit__` won't get called if `__aenter__`
        # fails). In turn, this avoids asyncio debug messages like the
        # following:
        #
        #   "[asyncio] Future exception was never retrieved"
        #
        # See also: https://docs.python.org/3/library/asyncio-dev.html#detect-never-retrieved-exceptions
        if not self._connected.done() or self._connected.exception() is not None:
            return
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self._disconnected.set_result(rc)
        else:
            self._disconnected.set_exception(MqttCodeError(rc, "Unexpected disconnect"))

    def _on_subscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        granted_qos: Union[Tuple[int], List[mqtt.ReasonCodes]],
        properties: Optional[mqtt.Properties] = None,
    ) -> None:
        try:
            fut = self._pending_subscribes.pop(mid)
            if not fut.done():
                fut.set_result(granted_qos)
        except KeyError:
            MQTT_LOGGER.error(f'Unexpected message ID "{mid}" in on_subscribe callback')

    def _on_unsubscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        properties: Optional[mqtt.Properties] = None,
        reasonCodes: Optional[Union[List[mqtt.ReasonCodes], mqtt.ReasonCodes]] = None,
    ) -> None:
        try:
            self._pending_unsubscribes.pop(mid).set()
        except KeyError:
            MQTT_LOGGER.error(
                f'Unexpected message ID "{mid}" in on_unsubscribe callback'
            )

    def _on_publish(self, client: mqtt.Client, userdata: Any, mid: int) -> None:
        try:
            self._pending_publishes.pop(mid).set()
        except KeyError:
            # Do nothing since [2] may call on_publish before it even returns.
            # That is, the message may already be published before we even get a
            # chance to set up the 'pending_call' logic.
            pass

    def _on_socket_open(
        self, client: mqtt.Client, userdata: Any, sock: _PahoSocket
    ) -> None:
        def cb() -> None:
            # client.loop_read() may raise an exception, such as BadPipe. It's
            # usually a sign that the underlaying connection broke, therefore we
            # disconnect straight away
            try:
                client.loop_read()
            except Exception as exc:
                if not self._disconnected.done():
                    self._disconnected.set_exception(exc)

        self._loop.add_reader(sock.fileno(), cb)
        # paho-mqtt calls this function from the executor thread on which we've called
        # `self._client.connect()` (see [3]), so we create a callback function to schedule
        # `_misc_loop()` and run it on the loop thread-safely.
        def create_task_cb() -> None:
            self._misc_task = self._loop.create_task(self._misc_loop())

        self._loop.call_soon_threadsafe(create_task_cb)

    def _on_socket_close(
        self, client: mqtt.Client, userdata: Any, sock: _PahoSocket
    ) -> None:

        fileno = sock.fileno()
        if fileno > -1:
            self._loop.remove_reader(fileno)
        if self._misc_task is not None and not self._misc_task.done():
            self._loop.call_soon_threadsafe(self._misc_task.cancel)

    def _on_socket_register_write(
        self, client: mqtt.Client, userdata: Any, sock: _PahoSocket
    ) -> None:
        def cb() -> None:
            # client.loop_write() may raise an exception, such as BadPipe. It's
            # usually a sign that the underlaying connection broke, therefore we
            # disconnect straight away
            try:
                client.loop_write()
            except Exception as exc:
                if not self._disconnected.done():
                    self._disconnected.set_exception(exc)

        self._loop.add_writer(sock, cb)

    def _on_socket_unregister_write(
        self, client: mqtt.Client, userdata: Any, sock: _PahoSocket
    ) -> None:
        self._loop.remove_writer(sock)

    async def _misc_loop(self) -> None:
        while self._client.loop_misc() == mqtt.MQTT_ERR_SUCCESS:
            await asyncio.sleep(1)

    async def __aenter__(self) -> "Client":
        """Connect to the broker."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        """Disconnect from the broker."""
        # Early out if already disconnected...
        if self._disconnected.done():
            disc_exc = self._disconnected.exception()
            if disc_exc is not None:
                # ...by raising the error that caused the disconnect
                raise disc_exc
            # ...by returning since the disconnect was intentional
            return
        # Try to gracefully disconnect from the broker
        try:
            await self.disconnect()
        except MqttError as error:
            # We tried to be graceful. Now there is no mercy.
            MQTT_LOGGER.warning(
                f'Could not gracefully disconnect due to "{error}". Forcing disconnection.'
            )
            await self.force_disconnect()


def _set_client_socket_defaults(
    client_socket: Optional[_PahoSocket], socket_options: Iterable[SocketOption]
) -> None:
    # Note that socket may be None if, e.g., the username and
    # password combination didn't work. In this case, we return early.
    if client_socket is None:
        return
    # Furthermore, paho sometimes gives us a socket wrapper instead of
    # the raw socket. E.g., for WebSocket-based connections.
    if not isinstance(client_socket, socket.socket):
        return
    # At this point, we know that we got an actual socket. We change
    # some of the default options.
    for socket_option in socket_options:
        client_socket.setsockopt(*socket_option)
