
# Azure Bootcamp VM Setup: Hosting a Static Web Page with NGINX

This walkthrough explains how I (Kanan 🚀) deployed a Linux-based virtual machine (VM) on Microsoft Azure to serve a static website using NGINX. The goal was to showcase my name and photo on a simple HTML page hosted from the cloud. All operations were performed via terminal tools like **PuTTY** and **WinSCP**—no browser consoles involved.

---

## 🛠️ Tools & Technologies Used

* **Microsoft Azure** – Cloud platform where the VM was created
* **Ubuntu 24.04 LTS** – Operating system on the virtual machine
* **PuTTY** – Used to connect securely via SSH
* **WinSCP** – Transferred local files to the remote server
* **NGINX** – Lightweight web server for serving static content
* **Shell (CLI)** – Configurations done entirely through command-line interface

---

## ☁️ Azure VM Details

* **VM Name:** `bootcamp-vm`
* **Public IP:** `http://20.193.143.123/`
* **OS Version:** Ubuntu 24.04.2 LTS
* **Size:** B1s instance – small and efficient for lightweight hosting

---

## 🔗 Connecting to Your Virtual Machine

### Step 1: SSH Key (if needed)

If key-based authentication is preferred, generate a key pair using PuTTYgen.

### Step 2: SSH via PuTTY

* **Host:** `20.193.143.123`
* **Port:** `22`
* **Key File:** Load your `.ppk` file if you're using one
* Confirm the SSH host fingerprint when prompted (⚠️ Always verify)

### Step 3: Login Info

* **Username:** `kanan`
* **Password:** *(as set during Azure VM creation)*

---

## 🧱 Initial Server Configuration

### Install NGINX

```bash
sudo apt update && sudo apt install nginx -y
```

### Confirm It’s Running

```bash
systemctl status nginx
```

Look for `Active: running` and try opening your public IP to confirm.

---

## 📂 Upload HTML and Image

Navigate to the server's root web folder:

```bash
cd /var/www/html/
```

Upload your photo (e.g. `Kanan.jpg`) using **WinSCP** into this folder.

Then, create a custom HTML file:

```bash
sudo nano index.html
```

Paste this HTML:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Kanan's Azure Page</title>
  </head>
  <body style="text-align:center; font-family:Arial;">
    <h1>Hey there, I’m Kanan 🚀</h1>
    K<img src="Kanan.jpg" alt="Kanan's Photo" width="300"
    <p>This static page is live from my Azure VM 🎯</p>
  </body>
</html>
```

Save and exit with `CTRL + O`, `ENTER`, and `CTRL + X`.

Now open [http://20.193.143.123/](http://20.193.143.123/) in your browser to view it live.

---

## 🗂️ Uploading Files with WinSCP

1. Open **WinSCP** and log in with your VM credentials.
2. Navigate to `/var/www/html/`.
3. Upload your image (e.g. `Kanan.jpg`) here.

Now your image is live at:

```
http://20.193.143.123/Kanan.jpg
```

---

## ✅ What This Teaches You

* How to create and connect to an Azure-hosted Linux VM
* SSH into a server using **PuTTY**
* Upload static files with **WinSCP**
* Install and configure **NGINX**
* Serve HTML and images from the cloud
* Get closer to real-world DevOps workflows 🚀

---

## 🧭 Optional Next Steps

* Enable `ufw` and restrict to HTTP/HTTPS only
* Map a custom domain to your Azure IP
* Install an SSL certificate using Let’s Encrypt

---

## 🖼️ Final Result

![screenshot](screenshot-placeholder.png)

*"Behind every server is someone bold enough to build it."* – Kanan

---

**Built with curiosity, commands, and coffee.**

