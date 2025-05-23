# FILE: zidoc_utils/preprocessor.py
from collections import defaultdict
from datetime import datetime

def compute_idoc_statistics(idoc_array: list[dict]) -> dict:
    """Runs all central preprocessing and returns reusable metrics for all 5 ideas"""
    stats = {
        "total": len(idoc_array),
        "status_counts": defaultdict(int),
        "mestyp_counts": defaultdict(int),
        "idoctp_counts": defaultdict(int),
        "partners": defaultdict(int),
        "daily_counts": defaultdict(int),
        "segments": defaultdict(int),
        "segment_samples": defaultdict(list),
        "delays": []
    }

    for entry in idoc_array:
        # 1. Status distribution
        status = entry.get("EDIDC_STATUS")
        if status:
            stats["status_counts"][status] += 1

        # 2. Message type distribution
        mestyp = entry.get("EDIDC_MESTYP")
        if mestyp:
            stats["mestyp_counts"][mestyp] += 1

        # 3. IDOCTP type distribution
        idoctp = entry.get("EDIDC_IDOCTP")
        if idoctp:
            stats["idoctp_counts"][idoctp] += 1

        # 4. Partner combinations
        snd = entry.get("EDIDC_SNDPRN")
        rcv = entry.get("EDIDC_RCVPRN")
        if snd and rcv:
            key = f"{snd} -> {rcv}"
            stats["partners"][key] += 1

        # 5. Daily volume
        date = entry.get("EDIDC_CREDAT")
        if date:
            stats["daily_counts"][date] += 1

        # 6. Segment usage
        segnam = entry.get("EDID4_SEGNAM")
        if segnam:
            stats["segments"][segnam] += 1
            if len(stats["segment_samples"][segnam]) < 2:
                stats["segment_samples"][segnam].append(entry.get("EDID4_SDATA", ""))

        # 7. Delay between creation and update
        cre_date = entry.get("EDIDC_CREDAT")
        cre_time = entry.get("EDIDC_CRETIM")
        upd_date = entry.get("EDIDC_UPDDAT")
        upd_time = entry.get("EDIDC_UPDTIM")

        if cre_date and cre_time and upd_date and upd_time:
            try:
                created_dt = datetime.strptime(f"{cre_date} {cre_time}", "%Y-%m-%d %H:%M:%S")
                updated_dt = datetime.strptime(f"{upd_date} {upd_time}", "%Y-%m-%d %H:%M:%S")
                delay = (updated_dt - created_dt).total_seconds()
                stats["delays"].append({
                    "DOCNUM": entry.get("EDIDC_DOCNUM"),
                    "delay_seconds": delay,
                    "created": f"{cre_date} {cre_time}",
                    "updated": f"{upd_date} {upd_time}"
                })
            except Exception:
                continue
    print(f"Stats Calc Check : \n {stats} \n ")

    return stats
