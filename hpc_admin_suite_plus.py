
import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ------------------------
# App Config & Header
# ------------------------
st.set_page_config(page_title="HPC Admin Suite • Guided", layout="wide")
st.title("🌟 HPC Admin Suite (Guided Edition)")
st.caption("A friendly demo of three core workflows for an HPC Systems Administrator: Slurm Queue, GPU Inventory, and RAID/NFS Health.")

# ------------------------
# Sidebar Navigation
# ------------------------
section = st.sidebar.radio("Navigate", [
    "🏠 Home (Start Here)",
    "1) Slurm Queue Mini‑Dashboard",
    "2) GPU Inventory Reporter",
    "3) RAID/NFS Health Snapshot",
    "📚 Glossary & How‑To (Plain English)"
])

# ------------------------
# Helper: Pretty info blocks
# ------------------------
def info_card(title, bullets):
    st.markdown(f"### {title}")
    for b in bullets:
        st.markdown(f"- {b}")

def demo_or_real_note():
    st.info("**Demo data provided.** You can paste your own CSV/JSON exports to simulate real environments.")

# ------------------------
# HOME
# ------------------------
if section.startswith("🏠"):
    st.subheader("Welcome")
    st.write("""
This app shows **three practical tasks**  
Each page explains **what the tool does**, **why it matters**, and **how to use it** (no prior knowledge needed).
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 1) Slurm Queue Mini‑Dashboard")
        st.write("See who is running jobs, who is waiting, and which partition (CPU vs GPU) is busy.")
    with col2:
        st.markdown("#### 2) GPU Inventory Reporter")
        st.write("Summarize GPU node details: model, count, driver version, CUDA version. Flags mismatches.")
    with col3:
        st.markdown("#### 3) RAID/NFS Health Snapshot")
        st.write("Check storage health for RAID arrays and review NFS exports (shared folders).")

    st.markdown("---")
    st.markdown("### How to Use This App")
    st.write("""
1. Choose a tool from the left sidebar.  
2. Read the short **What is this?** box at the top of each page.  
3. Use the **demo data** or **paste your own**.  
4. Review the **key indicators** and **plain‑English takeaways**.  
    """)

    st.markdown("### Who is this for?")
    st.write("""
- **Non‑technical viewers:** Learn what an HPC admin does via simple dashboards.  
- **Faculty/Researchers:** Understand queues, GPUs, and shared storage at a glance.  
    """)

# ------------------------
# 1) SLURM QUEUE MINI‑DASHBOARD
# ------------------------
elif section.startswith("1)"):
    st.header("1) Slurm Queue Mini‑Dashboard")
    st.markdown("**What is this?** Slurm is a system that fairly shares computers in a cluster. Jobs wait in a line (queue) until resources (CPUs/GPUs) are free.")
    st.markdown("**Why it matters:** Researchers want to know *who is running*, *who is waiting*, and *how long* it might take.")
    demo_or_real_note()

    default_df = pd.DataFrame({
        "job_id":[101,102,103,104,105,106],
        "user":["pi","grad1","grad2","pi","guest","grad1"],
        "partition":["cpu","gpu","gpu","gpu","cpu","cpu"],
        "state":["RUNNING","PENDING","RUNNING","PENDING","COMPLETED","RUNNING"],
        "req_gpus":[0,1,2,1,0,0],
        "elapsed_sec":[3600,0,7200,0,5400,1200],
        "submit_time":[
            "2025-08-27 09:00","2025-08-27 10:00","2025-08-27 08:30",
            "2025-08-27 10:15","2025-08-27 07:50","2025-08-27 11:00"
        ]
    })

    with st.expander("📥 Load Data (Use demo or paste your own `squeue/sacct` CSV)"):
        use_custom = st.checkbox("Paste custom CSV", value=False)
        if use_custom:
            csv_text = st.text_area(
                "Columns required: job_id,user,partition,state,req_gpus,elapsed_sec,submit_time",
                default_df.to_csv(index=False), height=180
            )
            try:
                df = pd.read_csv(pd.io.common.StringIO(csv_text))
            except Exception as e:
                st.error(f"Could not parse CSV: {e}")
                df = default_df.copy()
        else:
            df = default_df.copy()

    # Coerce types
    if "submit_time" in df.columns:
        try:
            df["submit_time"] = pd.to_datetime(df["submit_time"])
        except Exception:
            pass

    st.subheader("Queue Table")
    st.dataframe(df, use_container_width=True)

    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        user_filter = st.selectbox("Filter by user", ["All"]+sorted(df["user"].unique().tolist()))
    with colf2:
        part_filter = st.selectbox("Partition", ["All"]+sorted(df["partition"].unique().tolist()))
    with colf3:
        state_filter = st.selectbox("State", ["All"]+sorted(df["state"].unique().tolist()))

    f = df.copy()
    if user_filter != "All": f = f[f["user"]==user_filter]
    if part_filter != "All": f = f[f["partition"]==part_filter]
    if state_filter != "All": f = f[f["state"]==state_filter]

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Running", int((f["state"]=="RUNNING").sum()))
    with k2: st.metric("Pending", int((f["state"]=="PENDING").sum()))
    with k3: st.metric("Completed", int((f["state"]=="COMPLETED").sum()))
    with k4: st.metric("Avg Elapsed (min)", round((f["elapsed_sec"].mean() or 0)/60, 1))

    st.subheader("State Distribution")
    st.bar_chart(f.groupby("state").size())

    st.subheader("Longest Pending Jobs")
    pending = f[f["state"]=="PENDING"].copy()
    if "submit_time" in pending.columns:
        try:
            pending["pending_minutes"] = (pd.Timestamp.now() - pending["submit_time"]).dt.total_seconds()/60
        except Exception:
            pending["pending_minutes"] = 0
    else:
        pending["pending_minutes"] = 0
    st.dataframe(pending.sort_values("pending_minutes", ascending=False), use_container_width=True)

    st.markdown("---")
    st.markdown("**Plain‑English Takeaway:**")
    st.write("""
- **Running** = jobs currently using the cluster.  
- **Pending** = jobs waiting their turn (common on a busy system).  
- **Partitions** separate CPU vs GPU jobs so the right hardware is used.  
- If **Pending** is high or wait times are long, consider adjusting priorities or adding resources to that partition.
    """)

# ------------------------
# 2) GPU INVENTORY REPORTER
# ------------------------
elif section.startswith("2)"):
    st.header("2) GPU Inventory Reporter")
    st.markdown("**What is this?** A quick way to see which GPU models and driver versions your nodes are running.")
    st.markdown("**Why it matters:** Mixed driver or CUDA versions can break jobs or cause weird errors for researchers.")
    demo_or_real_note()

    sample = [
        {"node":"gpu01","gpus":4,"model":"A100-40GB","driver":"535.129","cuda":"12.2"},
        {"node":"gpu02","gpus":4,"model":"A100-40GB","driver":"535.129","cuda":"12.2"},
        {"node":"gpu03","gpus":2,"model":"RTX 6000 Ada","driver":"550.54","cuda":"12.4"},
        {"node":"gpu04","gpus":4,"model":"A100-40GB","driver":"535.129","cuda":"12.2"}
    ]

    with st.expander("📥 Paste or edit your Inventory JSON"):
        raw = st.text_area("Example structure shown below:", json.dumps(sample, indent=2), height=220)

    try:
        data = json.loads(raw)
        df = pd.DataFrame(data)
        st.subheader("Inventory Table")
        st.dataframe(df, use_container_width=True)

        st.subheader("Total GPUs by Model")
        st.bar_chart(df.groupby("model")["gpus"].sum())

        st.subheader("Health Checks (Plain English)")
        driver_count = df["driver"].nunique()
        cuda_count = df["cuda"].nunique()
        if driver_count > 1:
            st.warning("⚠️ Drivers are NOT uniform across nodes. Consider standardizing to reduce bugs.")
        else:
            st.success("✅ Driver versions look uniform — good for consistency.")
        if cuda_count > 1:
            st.info("ℹ️ CUDA versions differ. That can be fine, but shared environments usually prefer one version.")
        st.caption(f"Models detected: {df['model'].nunique()} • Driver variants: {driver_count} • CUDA variants: {cuda_count}")
    except Exception as e:
        st.error(f"Invalid JSON format: {e}")

    st.markdown("---")
    st.markdown("**Plain‑English Takeaway:**")
    st.write("""
- **Model** = the kind of GPU (e.g., A100 vs RTX 6000). Some are faster or have more memory.  
- **Driver** = the software that lets the OS talk to the GPU. Same drivers across nodes = fewer surprises.  
- **CUDA** = toolkit for GPU computing. Keeping versions consistent helps prevent job crashes.
    """)

# ------------------------
# 3) RAID / NFS HEALTH SNAPSHOT
# ------------------------
else:
    st.header("3) RAID/NFS Health Snapshot (Simulator)")
    st.markdown("**What is this?** A simple way to review storage health (RAID arrays) and shared folders (NFS exports).")
    st.markdown("**Why it matters:** If a RAID array is degraded, data is at risk and performance drops. NFS controls who can see shared research data.")
    demo_or_real_note()

    raid_default = pd.DataFrame([
        {"array":"/dev/md0","level":"RAID10","status":"clean","devices":4},
        {"array":"/dev/md1","level":"RAID6","status":"degraded","devices":8}
    ])
    nfs_default = pd.DataFrame([
        {"export":"/data","clients":"lab-subnet","opts":"rw,no_root_squash"},
        {"export":"/scratch","clients":"campus","opts":"rw,async"}
    ])

    with st.expander("📥 Paste custom RAID CSV (or use demo)"):
        use_custom_raid = st.checkbox("Paste custom RAID CSV", key="raidcsv")
        if use_custom_raid:
            raid_csv = st.text_area("Columns: array,level,status,devices", raid_default.to_csv(index=False), height=140)
            try:
                raid = pd.read_csv(pd.io.common.StringIO(raid_csv))
            except Exception as e:
                st.error(f"Could not parse RAID CSV: {e}")
                raid = raid_default.copy()
        else:
            raid = raid_default.copy()

    st.subheader("RAID Arrays")
    st.dataframe(raid, use_container_width=True)

    with st.expander("📥 Paste custom NFS CSV (or use demo)"):
        use_custom_nfs = st.checkbox("Paste custom NFS CSV", key="nfscsv")
        if use_custom_nfs:
            nfs_csv = st.text_area("Columns: export,clients,opts", nfs_default.to_csv(index=False), height=120)
            try:
                nfs = pd.read_csv(pd.io.common.StringIO(nfs_csv))
            except Exception as e:
                st.error(f"Could not parse NFS CSV: {e}")
                nfs = nfs_default.copy()
        else:
            nfs = nfs_default.copy()

    st.subheader("NFS Exports")
    st.dataframe(nfs, use_container_width=True)

    st.subheader("Health Summary")
    if "degraded" in raid["status"].astype(str).str.lower().values:
        st.error("Degraded RAID array(s) detected. Plan a rebuild/replacement and verify backups.")
    else:
        st.success("All RAID arrays look healthy.")
    st.download_button("⬇️ Download NFS exports CSV", nfs.to_csv(index=False), "nfs_exports.csv")

    st.markdown("---")
    st.markdown("**Plain‑English Takeaway:**")
    st.write("""
- **RAID**: Stores the same data across multiple disks so the system can survive a disk failure.  
- **Status = degraded**: One or more disks failed; replace and rebuild ASAP.  
- **NFS**: The shared folders researchers mount on their computers. Check who can access what and with which options.
    """)

# ------------------------
# GLOSSARY & HOW‑TO
# ------------------------
if section.endswith("How‑To (Plain English)"):
    st.header("📚 Glossary & How‑To (Plain English)")
    st.write("Short, friendly definitions + where they appear in this app.")

    st.markdown("### Slurm (Job Scheduler)")
    st.write("Shares cluster computers fairly among jobs. **Used in:** Slurm Queue Mini‑Dashboard.")

    st.markdown("### Partition (CPU vs GPU)")
    st.write("A group of machines for a specific type of job. **Used in:** Queue filters.")

    st.markdown("### GPU Model / Driver / CUDA")
    st.write("Model = hardware type; Driver = OS interface; CUDA = GPU computing toolkit. **Used in:** GPU Inventory.")

    st.markdown("### RAID")
    st.write("Keeps data safe by spreading it across disks. If one fails, data survives. **Used in:** RAID Health.")

    st.markdown("### NFS (Network File System)")
    st.write("Lets many machines share the same folder over the network. **Used in:** NFS Exports.")

    st.markdown("### Tips for Non‑Technical Users")
    st.write("""
- Green/Success messages = good; Red/Warning = needs attention.  
- If you see **Pending** jobs for a long time, talk to the admin about resources/queue policies.  
- If **RAID is degraded**, don't ignore it — plan a fix and check backups.  
- Keep **driver/CUDA versions** consistent to avoid surprise errors.
    """)
