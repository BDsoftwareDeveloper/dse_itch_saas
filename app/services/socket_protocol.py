import struct
import logging
import sys
import os
import errno

logger = logging.getLogger("protocol_logout")
event_logger = logging.getLogger("protocol_login")

def protocol_login(server, client_socket, sequence_number=1):
    """
    Perform protocol login after socket connection.
    :param server: Server SQLAlchemy model instance (with username/password/etc)
    :param client_socket: The open socket connection to the server
    :param sequence_number: Sequence number for login (default 1)
    :return: dict with login result/status
    """
    session_id = ' ' * 10
    payload_format = '!Hc6s10s10s20s'
    payload = struct.pack(
        payload_format,
        47,
        'L'.encode(),
        server.username.encode(),
        server.password.encode(),
        session_id.rjust(10).encode(),
        str(sequence_number).rjust(20).encode()
    )
    client_socket.sendall(payload)
    # Decode for logging
    decoded_payload = struct.unpack(payload_format, payload)
    decoded_data = {
        'Packet Length': decoded_payload[0],
        'Packet Type': decoded_payload[1].decode(),
        'Username': decoded_payload[2].decode('utf-8').rstrip('\x00'),
        'Password': decoded_payload[3].decode('utf-8').rstrip('\x00'),
        'Requested Session': decoded_payload[4].decode(),
        'Requested Sequence Number': decoded_payload[5].decode()
    }
    event_logger.info(f"Login Request Packet : {decoded_data}")

    # Optionally, wait for a response from the server
    try:
        # response = client_socket.recv(1024)
        # return {"status": "sent", "login_packet": decoded_data, "response": response.hex()}
        return {"status": "sent", "login_packet": decoded_data}
    except Exception as e:
        return {"status": "sent", "login_packet": decoded_data, "response": f"Error receiving: {e}"}

def send_logout_request(client_socket):
    try:
        if client_socket.fileno() >= 0:
            payload_format = '!Hc'
            payload = struct.pack(
                payload_format,
                1,
                'O'.encode(),
            )
            client_socket.sendall(payload)
            logger.info("Logout request sent successfully")
            # Decode for logging
            decoded_payload = struct.unpack(payload_format, payload)
            decoded_data = {
                'Packet Length': decoded_payload[0],
                'Packet Type': decoded_payload[1].decode(),
            }
            event_logger.info(f"Logout Request Packet : {decoded_data}")
        else:
            logger.info("Socket is not alive at this moment to send logout packet")
    except Exception as e:
        exception_message = str(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        logger.error(
            f"An Exception Occurred. Type: {exception_type}. Arguments: [{exception_message}]. "
            f"File Name: {filename}, Line no: {exception_traceback.tb_lineno}"
        )

def send_client_heartbeat(client_socket, server_type):
    try:
        if client_socket.fileno() >= 0:
            payload = struct.pack(
                '!Hc',
                1,
                'R'.encode(),
            )
            client_socket.sendall(payload)
        else:
            logger.info("Socket is not alive at this moment to send heartbeat packet")
            # heartbeat_socket_close_task(server_type=server_type)  # Commented out as requested

    except IOError as e:
        logger.error(f"Broken pipe error occurred: {e}")
        if e.errno == errno.EPIPE:
            if client_socket.fileno() >= 0:
                client_socket.close()
                # heartbeat_socket_close_task(server_type=server_type)  # Commented out as requested
                logger.info("Socket closed from client heartbeat pipe error")
    except Exception as e:
        exception_message = str(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        logger.error(
            f"An Exception Occurred. Type: {exception_type}. Arguments: [{exception_message}]. "
            f"File Name: {filename}, Line no: {exception_traceback.tb_lineno}"
        )
        
        
        
def read_packet_by_length(client_socket):
    """
    Reads a packet from the socket based on the length specified in the first 2 bytes.
    Returns the full packet as bytes, or None if the socket closes before a full packet is received.
    """
    try:
        header = client_socket.recv(2)
        if len(header) < 2:
            logger.error("Failed to read packet length header")
            raise Exception("Failed to read packet length header")
        packet_length = struct.unpack('!H', header)[0]
        remaining = packet_length - 2
        logger.debug(f"read_packet_by_length: header={header.hex()} packet_length={packet_length} remaining={remaining}")

        if remaining <= 0:
            return header

        data = b''
        while remaining > 0:
            chunk = client_socket.recv(remaining)
            logger.debug(f"read_packet_by_length: got chunk={chunk.hex()} remaining={remaining}")
            if not chunk:
                logger.warning(f"Socket closed before full packet received. Header: {header.hex()}, got {len(data)} of {remaining} bytes")
                return None
            data += chunk
            remaining -= len(chunk)
        return header + data
    except Exception as e:
        logger.error(f"Exception in read_packet_by_length: {e}")
        return None