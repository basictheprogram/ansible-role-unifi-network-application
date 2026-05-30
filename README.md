# Ansible Role: unifi_network_application

[![Build Status][build_badge]][build_link]
[![Ansible Galaxy][galaxy_badge]][galaxy_link]

> **Fork notice:** This role is a fork of
> [tigattack/ansible-role-unifi-network-application](https://github.com/tigattack/ansible-role-unifi-network-application)
> by [tigattack](https://github.com/tigattack). Full credit to tigattack for the
> original design and implementation. This fork is maintained independently at
> [basictheprogram/ansible-role-unifi-network-application](https://github.com/basictheprogram/ansible-role-unifi-network-application).
>
> **Issues:** Please open issues against this fork. If the fix applies to the
> upstream role as well, a pull request will be submitted to
> [tigattack's repository](https://github.com/tigattack/ansible-role-unifi-network-application).

Deploy [UniFi Network application](https://github.com/linuxserver/docker-unifi-network-application) in Docker

Install the role: `ansible-galaxy role install basictheprogram.unifi_network_application`

See [Example Playbooks](#example-playbooks) below.

## Requirements

* Ansible core >= 2.20
* Docker on the target host. Recommended: [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker)
* [community.docker](https://galaxy.ansible.com/ui/repo/published/community/docker/) Ansible collection — see [requirements.yml](requirements.yml)
* A chosen data path on the host

## Supported Platforms

| OS     | Versions                       |
|--------|--------------------------------|
| Debian | bookworm (12), trixie (13)     |
| Ubuntu | jammy (22.04), noble (24.04), resolute (26.04) |

## Task Flow

1. **Preflight** — asserts Ansible >= 2.20, supported architecture (amd64/arm64), and that both required secrets are set
2. **User/group lookup** — resolves UID/GID for the configured user and group
3. **Directory creation** — ensures `base_path/app` and `base_path/db` exist with correct ownership
4. **MongoDB init script** — copies `mongo-init.sh` to the DB data path
5. **Docker network** — creates the Docker network if absent
6. **Container deploy** — starts `unifi-mongo`, `unifi-network-application`, and optionally `mongo-express`

## Role Variables

> [!TIP]
> Run `ansible-doc -t role basictheprogram.unifi_network_application` to see full role documentation.

### Required

#### `unifi_network_application_mongo_password`

| Type   | Default |
|--------|---------|
| string | —       |

MongoDB password for the UniFi Network application user. **Required.**

#### `unifi_network_application_mongo_root_password`

| Type   | Default |
|--------|---------|
| string | —       |

MongoDB root password. **Required.**

---

### Paths and versions

#### `unifi_network_application_base_path`

| Type | Default      |
|------|--------------|
| path | `/opt/unifi` |

Base path for UniFi Network application data on the host.

#### `unifi_network_application_app_version`

| Type   | Default    |
|--------|------------|
| string | `10.3.58`  |

Docker image version for the UniFi Network application. Override in `host_vars` or `group_vars` to pin a different release. Avoid `latest` — use an explicit version tag.

#### `unifi_network_application_mongo_version`

| Type   | Default |
|--------|---------|
| string | `8.0`   |

Docker image version for MongoDB. Must be compatible with the UniFi version in use:

| UniFi version | Supported MongoDB |
|---------------|-------------------|
| 8.1+          | 3.6 – 7.0         |
| 9.0+          | 3.6 – 8.0         |

> [!WARNING]
> Do not use `latest` for MongoDB — it does not support automatic major version upgrades. Always pin to a major version (e.g. `8.0`).

---

### Identity

#### `unifi_network_application_user`

| Type | Default |
|------|---------|
| raw  | `1000`  |

User name or ID to run the containers as.

#### `unifi_network_application_group`

| Type | Default |
|------|---------|
| raw  | `1000`  |

Group name or ID to run the containers as.

---

### MongoDB

#### `unifi_network_application_mongo_dbname`

| Type   | Default |
|--------|---------|
| string | `unifi` |

MongoDB database name for UniFi Network application.

#### `unifi_network_application_mongo_user`

| Type   | Default |
|--------|---------|
| string | `unifi` |

MongoDB username for UniFi Network application.

#### `unifi_network_application_mongo_root_username`

| Type   | Default |
|--------|---------|
| string | `root`  |

MongoDB root username.

---

### Network and Docker

#### `unifi_network_application_docker_network`

| Type   | Default |
|--------|---------|
| string | `unifi` |

Name of the Docker network to connect the containers to.

#### `unifi_network_application_timezone`

| Type   | Default   |
|--------|-----------|
| string | `Etc/UTC` |

Timezone for the UniFi Network application. See [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List).

---

### Application tuning

#### `unifi_network_application_app_memlimit`

| Type | Default |
|------|---------|
| int  | `1024`  |

Memory limit in MB for the UniFi Network application container.

#### `unifi_network_application_app_memstartup`

| Type | Default |
|------|---------|
| int  | `1024`  |

JVM startup memory in MB for the UniFi Network application container.

---

### Deployment behaviour

#### `unifi_network_application_deployment_always_pull`

| Type | Default |
|------|---------|
| bool | `false` |

Always pull images before deploying. Useful when using `latest` or mutable tags.

#### `unifi_network_application_deployment_wait_for_health`

| Type | Default |
|------|---------|
| bool | `true`  |

Wait for containers to report healthy before continuing.

#### `unifi_network_application_prune_images`

| Type | Default |
|------|---------|
| bool | `false` |

Prune unused Docker images after deployment.

> [!WARNING]
> This role cannot filter pruned images — ALL unused images will be removed.

---

### Logging

#### `unifi_network_application_log_driver`

| Type   | Default     |
|--------|-------------|
| string | `json-file` |

Docker log driver for all containers.

#### `unifi_network_application_log_max_size`

| Type   | Default |
|--------|---------|
| string | `10m`   |

Maximum log file size before rotation.

#### `unifi_network_application_log_max_files`

| Type   | Default |
|--------|---------|
| string | `3`     |

Number of rotated log files to retain.

---

### Port exposure — UniFi application

All ports default to the standard UniFi port numbers. Set the `_expose` variable to `false` to suppress a port binding entirely.

| Variable | Default expose | Default port | Notes |
|----------|---------------|--------------|-------|
| `unifi_network_application_device_communication_expose` / `_port` | `true` | `8080` | Required for device communication |
| `unifi_network_application_web_admin_expose` / `_port` | `true` | `8443` | Web admin UI |
| `unifi_network_application_stun_expose` / `_port` | `true` | `3478` (UDP) | STUN |
| `unifi_network_application_device_discovery_expose` / `_port` | `true` | `10001` (UDP) | Device discovery |
| `unifi_network_application_l2_discovery_expose` / `_port` | `false` | `1900` (UDP) | L2 network discovery |
| `unifi_network_application_guest_portal_redirect_http_expose` / `_port` | `false` | `8880` | Guest portal HTTP redirect |
| `unifi_network_application_guest_portal_redirect_https_expose` / `_port` | `false` | `8843` | Guest portal HTTPS redirect |
| `unifi_network_application_mobile_speedtest_expose` / `_port` | `false` | `6789` | Mobile throughput test |
| `unifi_network_application_remote_syslog_expose` / `_port` | `false` | `5514` (UDP) | Remote syslog |

### Port exposure — MongoDB

#### `unifi_network_application_db_expose`

| Type | Default |
|------|---------|
| bool | `false` |

Expose MongoDB to the host (for external tools or mongo-express running outside the container network).

#### `unifi_network_application_db_port`

| Type | Default |
|------|---------|
| int  | `27017` |

Host port mapped to MongoDB's 27017 when `db_expose` is true.

---

### Optional: mongo-express

#### `unifi_network_application_mongo_express_enable`

| Type | Default |
|------|---------|
| bool | `false` |

Deploy a [mongo-express](https://github.com/mongo-express/mongo-express) container for browsing the MongoDB database.

#### `unifi_network_application_mongo_express_version`

| Type   | Default  |
|--------|----------|
| string | `latest` |

Docker image version for mongo-express.

#### `unifi_network_application_mongo_express_port`

| Type | Default |
|------|---------|
| int  | `8081`  |

Host port for the mongo-express web UI.

#### `unifi_network_application_mongo_express_extra_env`

| Type  | Default |
|-------|---------|
| dict  | `{}`    |

Extra environment variables for the mongo-express container.

---

### Extra environment variables

#### `unifi_network_application_app_extra_env`

| Type  | Default |
|-------|---------|
| dict  | `{}`    |

Extra environment variables for the UniFi Network application container.

#### `unifi_network_application_db_extra_env`

| Type  | Default |
|-------|---------|
| dict  | `{}`    |

Extra environment variables for the MongoDB container.

---

### MongoDB ulimits

#### `unifi_network_application_db_ulimits`

| Type      | Default |
|-----------|---------|
| list[str] | `[]`    |

Optional ulimits for the MongoDB container. Format: `nofile:262144:262144`.

---

## Example Playbooks

**Bare minimum:**

```yml
---
- name: Deploy UniFi Network Application
  hosts: server
  roles:
    - role: basictheprogram.unifi_network_application
      vars:
        unifi_network_application_mongo_password: _!CHANGEME!_
        unifi_network_application_mongo_root_password: _!CHANGEME!_
```

**With mongo-express and pinned versions:**

```yml
---
- name: Deploy UniFi Network Application
  hosts: server
  roles:
    - role: basictheprogram.unifi_network_application
      vars:
        unifi_network_application_app_version: "10.3.58"
        unifi_network_application_mongo_version: "8.0"
        unifi_network_application_mongo_password: _!CHANGEME!_
        unifi_network_application_mongo_root_password: _!CHANGEME!_
        unifi_network_application_timezone: America/Chicago
        unifi_network_application_mongo_express_enable: true
```

## License

MIT

[build_badge]:  https://img.shields.io/github/actions/workflow/status/basictheprogram/ansible-role-unifi-network-application/test.yml?branch=main&label=Lint%20%26%20Test
[build_link]:   https://github.com/basictheprogram/ansible-role-unifi-network-application/actions?query=workflow:Test
[galaxy_badge]: https://img.shields.io/ansible/role/d/basictheprogram/unifi_network_application
[galaxy_link]:  https://galaxy.ansible.com/ui/standalone/roles/basictheprogram/unifi_network_application/
