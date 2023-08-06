# Audiobomben senden

Synapse module to send audiobomb messages.

Compatible with Synapse v1.57.0 and later.

## Installation
Create a Database manually

From the virtual environment that you use for Synapse, install this module with:
```shell
pip install synapse-audiobomb
```
(If you run into issues, you may need to upgrade `pip` first, e.g. by running
`pip install --upgrade pip`)

Then alter your homeserver configuration, adding to your `modules` configuration:
```yaml
modules:
    - module: synapse_audiobomb_module.Audiobombs
    - config:
        host: localhost
        database: <databasename>
        user: <database_user>
        password: <password>
```

