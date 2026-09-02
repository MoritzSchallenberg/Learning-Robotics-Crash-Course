# Networking and SSH

{{ common }}

A robot is a computer you cannot sit in front of. Everything you do with it —
starting nodes, reading logs, editing code — happens over the network. This
page covers the minimum you need, plus the ROS 2 networking settings that cause
the most confusion.

## Learning objectives

After this page you can:

- explain what `ROS_DOMAIN_ID` does and when `ROS_LOCALHOST_ONLY` is wrong;
- connect to another machine with SSH and set up key-based login;
- read an IP address and a netmask, and say whether two machines are on the
  same subnet;
- explain why ROS 2 topics sometimes do not cross between two networks, and
  what a republisher does about it.

## Prerequisites

[Linux and the terminal](linux-terminal.md) and a working ROS 2 installation.

## ROS 2 network variables

ROS 2 nodes find each other by broadcasting on the network — there is no
central master. Two environment variables control that discovery, and getting
them wrong is the most common reason a robot "does not publish anything".

`ROS_DOMAIN_ID`
: An integer that partitions the network. Nodes only see each other if they
  share the same domain ID. Every machine that must talk to your robot needs
  the same value.

`ROS_LOCALHOST_ONLY`
: Set to `1`, this confines ROS 2 to the local machine. Useful when several
  people run simulations on the same lab network and you do not want to
  interfere with each other.

:::{danger}
`ROS_LOCALHOST_ONLY=1` overrides everything else. If it is set, your computer
cannot talk to a robot **no matter what `ROS_DOMAIN_ID` you choose**. Do not
set both when you want to control a robot from another machine.
:::

Set them in `~/.bashrc`:

```bash
# Simulation on one machine only, isolated from the lab network:
export ROS_LOCALHOST_ONLY=1

# Or: talking to a physical robot -- do NOT also set ROS_LOCALHOST_ONLY
export ROS_DOMAIN_ID=<your_id>
```

Ask your team which domain ID to use, or check the robot for a label. Picking
one at random works until two people pick the same one.

### Restricting discovery to one interface

{{ carologistics }}

If broadcasting across the whole lab network is a problem, the DDS
implementation can be told which interface to use. The Carologistics setup
configures Cyclone DDS with an XML file:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain Id="any">
    <General>
      <Interfaces>
        <NetworkInterface address="127.0.0.1"/>
      </Interfaces>
      <AllowMulticast>true</AllowMulticast>
      <EnableMulticastLoopback>true</EnableMulticastLoopback>
    </General>
  </Domain>
</CycloneDDS>
```

Save it as `~/cyclone_dds.xml` and register it in `~/.bashrc`:

```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///home/<username>/cyclone_dds.xml
```

The ROS 2 daemon caches discovery information, so restart it after changing
these:

```bash
ros2 daemon stop
```

:::{note}
The `127.0.0.1` address above confines ROS 2 to the local machine — the same
effect as `ROS_LOCALHOST_ONLY=1`, which is what the Carologistics lab setup
wants for local development. To talk to a robot, this must name the interface
that reaches the robot instead.
:::

## SSH

SSH gives you a terminal on another machine. You need three things: the
username on that machine, its IP address, and both machines on the same
network.

### Find the address and username

On the machine you want to connect **to**:

```bash
ip addr        # look for the "inet" address of your active interface
whoami         # the username
```

:::{tip}
`ifconfig` does the same job and appears in older guides, but it is not
installed by default on modern Ubuntu. `ip addr` is the current tool.
:::

### Connect

```bash
ssh <username>@<ip-address>
```

The first time, SSH asks you to confirm the host's key fingerprint. Type `yes`.

If you get `Connection refused`, the SSH *server* is not running on the target
machine:

```bash
# on the machine you want to connect TO
sudo apt install openssh-server
```

:::{note}
An SSH session belongs to one terminal. Every new terminal needs its own `ssh`
command. And if your Wi-Fi drops, the session dies — along with any unsaved
files and any node you started in it. For long-running work use a terminal
multiplexer such as `screen` or `tmux`, which survives a dropped connection.
:::

### Key-based login

Typing a password for every connection is tedious and encourages weak
passwords. Install a key instead.

On the machine you connect **from**:

```bash
ssh-keygen -t ed25519
ssh-copy-id -i ~/.ssh/id_ed25519.pub <username>@<ip-address>
```

You are asked for the remote password once, during `ssh-copy-id`. After that,
`ssh <username>@<ip-address>` logs you in with the key.

:::{tip}
Give the key a passphrase. It protects the key if your laptop is lost, and
`ssh-agent` means you only type it once per session.
:::

### Make it convenient

Add frequently used hosts to `~/.ssh/config`:

```text
Host myrobot
    HostName <ip-address>
    User <username>
```

Then `ssh myrobot` is enough.

### Editing code over SSH

VS Code's **Remote - SSH** extension opens a folder on the robot as if it were
local — editor, terminal and debugger all run against the remote machine.

1. Install the *Remote - SSH* extension (`Ctrl` + `Shift` + `X`).
2. Click the `><` icon in the bottom-left corner.
3. *Connect to Host…* → *+ Add New SSH Host…*
4. Enter `ssh <username>@<ip-address>` and choose `~/.ssh/config` to save it.
5. Select the host and connect, then open your workspace folder.

## Subnets, and why ROS 2 sometimes cannot cross them

An IP address is split into a *network* part and a *host* part; the netmask
says where the boundary is. A netmask of `255.255.255.0` (also written `/24`)
means the first three bytes identify the network and the last byte identifies
the machine:

```text
IP address    192.168.1.100    11000000.10101000.00000001.01100100
Netmask       255.255.255.0    11111111.11111111.11111111.00000000
Network       192.168.1.0      11000000.10101000.00000001.00000000
```

Two machines can talk directly only if that network part matches.

This matters for ROS 2 because **discovery does not cross subnets by default**.
A typical robot has an onboard computer connected to a robot base over Ethernet
(one subnet) and to your laptop over Wi-Fi (a different subnet). Topics
published by the base are visible on the Ethernet side and invisible to you —
even with the correct `ROS_DOMAIN_ID`, because the domain ID is not the
problem.

Check what you can see:

```bash
ip addr           # which subnets am I on?
ros2 topic list   # which topics can I actually see?
```

### The republisher pattern

The fix is a small node on the onboard computer that subscribes to the topics
on one interface and publishes them again. Because ROS 2 broadcasts to all
available interfaces, the republished topics appear on both networks.

This has a useful side effect: republishing only the topics you actually need
keeps camera and point cloud traffic off the Wi-Fi, which is usually the
bottleneck.

Your platform page documents the concrete republisher for your robot, if it
needs one.

## Task

:::{admonition} Task: connect to another machine
:class: task

Pair up with someone, or use a second machine or a virtual machine.

1. On machine B, install `openssh-server` and find its IP address and username.
2. From machine A, connect with `ssh` using the password.
3. Set up key-based login and confirm you can connect without a password.
4. Add machine B to `~/.ssh/config` and connect using the short name.
5. Set the same `ROS_DOMAIN_ID` on both machines. Run
   `ros2 run demo_nodes_cpp talker` on B and `ros2 topic list` on A.
6. Now set `ROS_LOCALHOST_ONLY=1` on machine A, open a **new** terminal, and
   run `ros2 topic list` again.
:::

:::{admonition} Expected result
:class: result

In step 5, machine A lists `/chatter` — a topic published on another computer
entirely. In step 6 it does not, which demonstrates that
`ROS_LOCALHOST_ONLY` overrides the domain ID.

Remember to unset it afterwards.
:::

## Common mistakes

**`ros2 topic list` is empty although both machines are on the network.**
In order of likelihood: `ROS_LOCALHOST_ONLY=1` is set; the domain IDs differ;
the machines are on different subnets; a firewall is blocking discovery.

**Changed a variable but nothing happened.**
Environment variables apply to terminals opened afterwards. Open a new terminal
and run `ros2 daemon stop`.

**`Permission denied (publickey)`.**
The key was not installed, or you copied the private key instead of the `.pub`.
Re-run `ssh-copy-id`.

**Losing work when the connection drops.**
Use `screen` or `tmux` on the robot for anything long-running.

## A note on internal networks

Team networks — the Wi-Fi names, the address ranges, the device credentials —
are **not** documented on this public site. Ask your team lead for the network
setup, and never commit those details to a public repository.

## Further reading

- [ROS 2: DDS tuning and networking](https://docs.ros.org/en/humble/How-To-Guides/DDS-tuning.html)
- [ROS 2: About domain IDs](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Domain-ID.html)
- [OpenSSH manual](https://www.openssh.com/manual.html)
