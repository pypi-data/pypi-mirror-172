# Scope
This tool is useful for monitoring traffic usage of iliad sim from a command line

# Install

- cd
- python -m venv .venv_iliad_conn
- source .venv_iliad_conn/bin/activate
- pip install iliadconn
- run iliadconn
- nano xxx.ini *insert username and password, there are on receipt of sim*
- re-run iliadconn
- enjoy result
- now you can add to gnome top panel using executor extension and set to run script every hour: .venv_iliad_conn/bin/iliadconn