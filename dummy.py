import datetime
import ctypes
import os
import sys

#hi
def set_system_date(new_date: datetime.datetime):
    """Sets the system date to the provided datetime object."""
    if sys.platform == "win32":
        # Windows API structure for system time
        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [
                ("wYear", ctypes.c_ushort),
                ("wMonth", ctypes.c_ushort),
                ("wDayOfWeek", ctypes.c_ushort),
                ("wDay", ctypes.c_ushort),
                ("wHour", ctypes.c_ushort),
                ("wMinute", ctypes.c_ushort),
                ("wSecond", ctypes.c_ushort),
                ("wMilliseconds", ctypes.c_ushort),
            ]
        
        # Windows uses UTC time for SetSystemTime
        utc_date = new_date.astimezone(datetime.timezone.utc)
        win_time = SYSTEMTIME(
            wYear=utc_date.year,
            wMonth=utc_date.month,
            wDayOfWeek=0,  # Ignored by SetSystemTime
            wDay=utc_date.day,
            wHour=utc_date.hour,
            wMinute=utc_date.minute,
            wSecond=utc_date.second,
            wMilliseconds=0
        )
        # Call the Windows API (Requires Administrator privileges)
        if not ctypes.windll.kernel32.SetSystemTime(ctypes.byref(win_time)):
            raise PermissionError("Failed to set Windows system time. Run script as Administrator.")
            
    elif sys.platform in ("linux", "darwin"):
        # Linux and macOS use the standard 'date' command (Requires sudo/root)
        # Format: MMDDhhmmYYYY
        formatted_time = new_date.strftime("%m%d%H%M%Y")
        exit_code = os.system(f"sudo date {formatted_time}")
        if exit_code != 0:
            raise PermissionError("Failed to set system time. Ensure you have sudo privileges.")

def change_computer_day(days_to_add: int):
    """Adjusts the system clock by a relative number of days."""
    current_time = datetime.datetime.now()
    target_time = current_time + datetime.timedelta(days=days_to_add)
    set_system_date(target_time)
    print(f"System date successfully changed to: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")

def increment_computer_day():
    """Increments the computer's actual system date by 1 day."""
    change_computer_day(1)

def decrement_computer_day():
    """Decrements the computer's actual system date by 1 day."""
    change_computer_day(-1)

increment_computer_day()