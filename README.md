# NetScope for Home Assistant

**NetScope** is a lightweight local network scanner and device tracker designed as a clean, native alternative to tools like Fing. It runs automated local network scans using **Nmap**, automatically mapping out your devices into Home Assistant's Device Registry with IP tracking, MAC address discovery, local hostname resolution, and manufacturer (OUI) lookup.

---

## Features

* **Automated Local Scans:** Scans your target subnet using asynchronous Nmap subprocesses without blocking Home Assistant.
* **Device Registry Integration:** Automatically registers discovered devices, linking them by MAC address and updating their states.
* **Rich Attributes:** Exposes IP addresses, MAC addresses, hardware manufacturers (vendors), and local hostnames.
* **Config Flow Support:** Easily set up, configure, and change your target subnet straight from the Home Assistant UI.

---

## Prerequisites

Because NetScope relies on Nmap to perform network sweeps, **Nmap must be installed on your host system**. 

* **Home Assistant OS / Supervised:** Most base systems include it, or it can be accessed via terminal add-ons if needed.
* **Home Assistant Container / Core (Linux):** Ensure `nmap` is installed via your system package manager (e.g., `sudo apt install nmap` or `sudo pacman -S nmap`).

---

## Installation (HACS)

You can easily install NetScope as a custom repository in HACS:

1. Open **HACS** in your Home Assistant instance.
2. Click on the three dots in the top-right corner and select **Custom repositories**.
3. Paste your GitHub repository URL (`https://github.com/hugo565/netscope`) and choose **Integration** as the category.
4. Click **Add**.
5. Find **NetScope** in the HACS store, click **Download**, and restart your Home Assistant instance.

---

## Configuration

1. Go to **Settings** > **Devices & Services** in Home Assistant.
2. Click **Add Integration** in the bottom right corner.
3. Search for **NetScope**.
4. Enter your target subnet (e.g., `192.168.1.0/24`) and submit.
