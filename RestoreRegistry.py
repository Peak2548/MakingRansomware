import ctypes
import sys
import winreg
import platform

def restore_security_features():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    def delete_registry_value(hkey, path, name):
        try:
            key = winreg.OpenKey(hkey, path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
        except FileNotFoundError:
            print(f"[-] Value already at default {name}")
        except Exception as e:
            print(f"Error {name}: {e}")

    try:
        defender_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
        rt_path = r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection"
        policy_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"

        delete_registry_value(winreg.HKEY_LOCAL_MACHINE, defender_path, "DisableAntiSpyware")

        delete_registry_value(winreg.HKEY_LOCAL_MACHINE, rt_path, "DisableRealtimeMonitoring")
        delete_registry_value(winreg.HKEY_LOCAL_MACHINE, rt_path, "DisableBehaviorMonitoring")
        delete_registry_value(winreg.HKEY_LOCAL_MACHINE, rt_path, "DisableOnAccessProtection")
        delete_registry_value(winreg.HKEY_LOCAL_MACHINE, rt_path, "DisableScanOnRealtimeEnable")

        delete_registry_value(winreg.HKEY_CURRENT_USER, policy_path, "DisableTaskMgr")
        delete_registry_value(winreg.HKEY_CURRENT_USER, policy_path, "DisableRegistryTools")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if platform.system() == "Windows":
        restore_security_features()