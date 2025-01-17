import win32pipe, win32file
# Validated & error checked.


class Pipe:
    def __init__(self, name : str, is_server : bool, max_buffer_size : int = 65536):
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

    def write(self, mid : str, msg : str):
        if len(mid) + len(msg)> self.max_buffer_size-1:
            raise IndexError("Sum of id and msg cannot exceed 65536 in length.")
        win32file.WriteFile(self.pipe, mid.encode())
        win32file.WriteFile(self.pipe, msg.encode())

    def read(self) -> tuple[str, str]:
        mid = win32file.ReadFile(self.pipe, self.max_buffer_size)[1].decode()
        msg = win32file.ReadFile(self.pipe, self.max_buffer_size)[1].decode()
        return mid, msg

    def close(self):
      if self.pipe is not None: # If creation fails, it is None.
          win32file.CloseHandle(self.pipe)
          self.pipe = None
