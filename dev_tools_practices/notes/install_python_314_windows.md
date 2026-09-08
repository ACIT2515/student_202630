# Python 3.14 Installation Windows 11

Updated: 2025/10/30

Python is now recommended to be installed with the "Python Install Manager" under Windows.

## Process

1. Uninstall your existing Python to avoid issues.

1. Install `Python Install Manager`:

   ```powershell
   winget install --name "Python Install Manager" -e --accept-package-agreements --disable-interactivity -s msstore
   ```

   May require you to accept sending your computer's country code to Microsoft.

1. Configure the Python Install Manager: 
   ```powershell
   pymanager install --configure -y
   ```

1. Install Python 3.14:

   ```powershell
   pymanager install 3.14
   ``` 


## Notes: 

1. These instructions use `pymanager` command rather than the `py` command specified in the documentation in case the `py` command is still mapped to the `python` launcher.

1. The `pip` command may no longer be in your path. If so, you can invoke `pip` using: `python -m pip`

## Documentation

1. [Get started with the new Python Installation Manager](https://www.infoworld.com/article/4001983/get-started-with-the-new-python-installation-manager.html)
1. [Python Setup and Usage](https://docs.python.org/3/using/index.html)
1. [Using Python on Windows](https://docs.python.org/3/using/windows.html)
1. [Python Install Manager Configuration](https://docs.python.org/3/using/windows.html#configuration)
1. [`winget` Install Command](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)