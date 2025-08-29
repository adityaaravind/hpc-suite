

---

# 🌟 HPC Admin Suite (Guided Edition)

> 📊 A simple, interactive way to understand what a **High-Performance Computing (HPC) Systems Administrator** does.
> Built with [Streamlit](https://streamlit.io/) so anyone — even without a technical background — can explore queues, GPUs, and storage health.

---

## ✨ What is this?

Running a **supercomputer (HPC cluster)** can sound complicated.
This project turns those tasks into **easy-to-read dashboards** that show:

1. 🚦 **Slurm Queue Mini-Dashboard** – Who’s running jobs, who’s waiting, and how busy the CPUs and GPUs are.
2. 🎮 **GPU Inventory Reporter** – What kinds of GPUs are in the cluster, how many there are, and whether their drivers match.
3. 💾 **RAID/NFS Health Snapshot** – Is the storage healthy? Which shared folders are available to researchers?

Think of it as **“Google Classroom” but for a supercomputer lab’s backend** — the admin sees what’s happening and keeps everything healthy.

---

## 🎯 Who is this for?

* 👩‍🎓 **Curious Students / Non-Technical Viewers**
  Learn how a supercomputer is managed with clear visuals instead of code dumps.
* 👨‍🏫 **Faculty / Researchers**
  Quickly check job queues, GPU availability, and shared storage without digging into the terminal.
* 💼 **Job Interview Prep**
  Show practical, hands-on familiarity with HPC administration in under 5 minutes.

---

## 🖥️ How it works (plain English)

* 🚦 **Jobs and Queues (Slurm):**
  Imagine students lining up at the library printers. Some are printing big jobs, others small. The queue decides *who goes first*. That’s what the Slurm dashboard shows for supercomputers.

* 🎮 **GPUs and Drivers:**
  A GPU is like the engine of a gaming PC or AI workstation. If some computers have different engines or drivers, things break. The GPU reporter checks if everything matches.

* 💾 **Storage (RAID + NFS):**
  RAID = making copies of data across disks, so nothing is lost if one fails.
  NFS = a shared Google Drive for the whole lab. The storage snapshot shows if disks are healthy and who can access the shared folders.

---

## 🚀 Quickstart

### Option 1: Run with **pipx** (recommended if pip is broken)

```bash
# Install pipx if not already
sudo apt update
sudo apt install -y pipx
python3 -m pipx ensurepath

# Install and run Streamlit
pipx install streamlit
pipx run streamlit run hpc_admin_suite_plus.py
```

### Option 2: Run with pip / virtual environment

```bash
git clone https://github.com/YOURUSERNAME/hpc-suite.git
cd hpc-suite

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
streamlit run hpc_admin_suite_plus.py
```

Then open the link shown in your terminal (usually `http://localhost:8501`) in a browser.

---

## 🌐 Deploy Online (Free!)

You can host this app for free on **Streamlit Community Cloud**:

1. Push this repo to GitHub.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → click **New App**.
3. Select your repo and set **`hpc_admin_suite_plus.py`** as the entry file.
4. Click Deploy 🚀

Now anyone can open your app in a browser with a shareable URL.

---

## 📖 Features in detail

### 🚦 1) Slurm Queue Mini-Dashboard

* Shows jobs that are **Running, Pending, Completed**.
* Filters by user, partition (CPU/GPU), and job state.
* Bar charts and tables to spot bottlenecks.
  👉 *Takeaway:* If lots of jobs are pending, the cluster may need more resources or queue tweaks.

### 🎮 2) GPU Inventory Reporter

* Paste or load a JSON list of GPU nodes.
* Summarizes total GPUs by model.
* Checks if **driver/CUDA versions** are consistent.
  👉 *Takeaway:* Mismatched drivers cause headaches — uniform setups = happy researchers.

### 💾 3) RAID/NFS Health Snapshot

* Shows if RAID arrays are **healthy or degraded**.
* Lists **NFS exports** (shared folders) and who can access them.
* Lets you download a copy of the export list.
  👉 *Takeaway:* A degraded RAID means a disk failed; fix it before another one goes down.

---

## 📚 Glossary (Simple)

* 🖥️ **HPC Cluster** – A bunch of powerful computers working together.
* 🚦 **Slurm** – The traffic cop that decides which jobs run first.
* 🎮 **GPU** – Super-fast processors (good at math and AI).
* 🧩 **Driver** – Software that makes hardware usable.
* ⚡ **CUDA** – Toolkit for running programs on GPUs.
* 💾 **RAID** – Backup method: data spread across many disks.
* 📂 **NFS** – A shared network folder for the whole lab.

---

## 🎨 Example Screenshot (conceptual)

```
🖥️ Slurm Queue Dashboard
-------------------------
Running Jobs: 3
Pending Jobs: 2
Completed: 1
Avg Elapsed: 45 min

📊 Bar Chart: RUNNING | PENDING | COMPLETED
```

---

## 💡 Why this project matters

Supercomputers run critical research in **physics, biology, medicine, and AI**.
Behind the scenes, admins make sure **jobs run smoothly, GPUs are consistent, and data is safe**.
This project shows that world in a way **anyone can click through and understand**.

---

## 🛠️ Tech Stack

* [Streamlit](https://streamlit.io/) – turns Python scripts into web apps.
* [Pandas](https://pandas.pydata.org/) – handles data tables.
* **Python 3.8+** – the language that powers it all.

---

## 👩‍💻 Author

Created by **Aditya Aravind** as part of HPC Systems Administration learning & interview prep.
Pull requests and feedback are welcome!

---

✨ Now, even if you’ve never touched a supercomputer before, you can **understand and demo HPC administration in 10 minutes.**

---

