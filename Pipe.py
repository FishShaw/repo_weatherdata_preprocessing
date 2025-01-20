import win32pipe, win32file
import logging
# Validated & error checked.


class Pipe:
    def __init__(self, name : str, is_server : bool, max_buffer_size : int = 131072):
        self.max_buffer_size = max_buffer_size
        self.is_server = is_server
        if is_server:
            self.pipe = win32pipe.CreateNamedPipe(
                fr'\\.\pipe\{name}',
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, max_buffer_size, max_buffer_size,
                0,
                None)
        else:
            self.pipe = win32file.CreateFile(
                fr'\\.\pipe\{name}',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            win32pipe.SetNamedPipeHandleState(self.pipe, win32pipe.PIPE_READMODE_MESSAGE, None, None)

    def connect(self):
        if self.is_server:
            win32pipe.ConnectNamedPipe(self.pipe, None)
        else:
            raise Exception("Only server needs to call this.")
        
    def peek(self) -> bool:
        return win32pipe.PeekNamedPipe(self.pipe, 0)[1] > 0

    def write(self, message_id: str, content: str):
        try:
            # 写入消息ID和分隔符
            win32file.WriteFile(self.pipe, message_id.encode('utf-8'))
            win32file.WriteFile(self.pipe, b'\0')
            
            # 写入消息内容和结束符
            win32file.WriteFile(self.pipe, content.encode('utf-8'))
            win32file.WriteFile(self.pipe, b'\0')
            
            logging.debug(f"Written message: {message_id}, content length: {len(content)}")
        except Exception as e:
            logging.error(f"Error writing to pipe: {e}")
            raise

    def read(self):
        try:
            message_id = b''
            while True:
                _, b = win32file.ReadFile(self.pipe, 1)
                if b == b'\0' or not b:
                    break
                message_id += b
                
            content = b''
            while True:
                _, b = win32file.ReadFile(self.pipe, 1)
                if b == b'\0' or not b:
                    break
                content += b
                
            return message_id.decode('utf-8'), content.decode('utf-8')
        except Exception as e:
            logging.error(f"Error reading from pipe: {e}")
            raise

    def close(self):
      if self.pipe is not None: # If creation fails, it is None.
          win32file.CloseHandle(self.pipe)
          self.pipe = None
