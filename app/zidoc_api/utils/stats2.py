import datetime

def generate_idoc_analytics2_html_report(idoc_data):
    """
    Generates an HTML analytics report from iDoc data (EDIDC and EDID4 combined records).
    
    Args:
        idoc_data (list): List of dictionaries containing iDoc records
        
    Returns:
        str: HTML content string suitable for email body
    """
    if not idoc_data:
        return "<h2>No iDoc Data Available</h2>"
    
    # Calculate statistics
    total_idocs = len(idoc_data)
    
    # Message type distribution
    mestyp_dist = {}
    idoctyp_dist = {}
    status_dist = {}
    direction_dist = {}
    date_dist = {}
    
    for record in idoc_data:
        # EDIDC fields
        mestyp = record.get('EDIDC_MESTYP', 'UNKNOWN')
        mestyp_dist[mestyp] = mestyp_dist.get(mestyp, 0) + 1
        
        idoctyp = record.get('EDIDC_IDOCTP', 'UNKNOWN')
        idoctyp_dist[idoctyp] = idoctyp_dist.get(idoctyp, 0) + 1
        
        status = record.get('EDIDC_STATUS', 'UNKNOWN')
        status_dist[status] = status_dist.get(status, 0) + 1
        
        direction = record.get('EDIDC_DIRECT', 'UNKNOWN')
        direction = "Outbound" if direction == "2" else "Inbound" if direction == "1" else direction
        direction_dist[direction] = direction_dist.get(direction, 0) + 1
        
        credat = record.get('EDIDC_CREDAT', 'UNKNOWN')
        date_dist[credat] = date_dist.get(credat, 0) + 1
    
    # Sort distributions by count
    mestyp_sorted = sorted(mestyp_dist.items(), key=lambda x: x[1], reverse=True)
    idoctyp_sorted = sorted(idoctyp_dist.items(), key=lambda x: x[1], reverse=True)
    status_sorted = sorted(status_dist.items(), key=lambda x: x[1], reverse=True)
    direction_sorted = sorted(direction_dist.items(), key=lambda x: x[1], reverse=True)
    date_sorted = sorted(date_dist.items(), key=lambda x: x[0], reverse=True)
    
    # Generate HTML
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>iDoc Analytics Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    margin-top: 30px;
                    color: #2980b9;
                }}
                h3 {{
                    color: #16a085;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                tr:hover {{
                    background-color: #e3f2fd;
                }}
                .summary-card {{
                    background: #f8f9fa;
                    border-left: 4px solid #3498db;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .highlight {{
                    font-weight: bold;
                    color: #e74c3c;
                }}
            </style>
        </head>
        <body>
            <h1>iDoc Processing Analytics Report</h1>
            <p>Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

            <div class="summary-card">
                <h2>Summary Overview</h2>
                <p>Total iDocs processed: <span class="highlight">{total_idocs}</span></p>
                <p>Date range: <span class="highlight">{date_sorted[-1][0] if date_sorted else 'N/A'}</span> to <span class="highlight">{date_sorted[0][0] if date_sorted else 'N/A'}</span></p>
            </div>
    
            <h2>Message Type Distribution</h2>
            <table>
                <thead>
                    <tr>
                        <th>Message Type</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(
                        f"<tr><td>{mestyp}</td><td>{count}</td><td>{round(count/total_idocs*100, 2)}%</td></tr>"
                        for mestyp, count in mestyp_sorted
                    )}
                </tbody>
            </table>
    
            <h2>iDoc Type Distribution</h2>
            <table>
                <thead>
                    <tr>
                        <th>iDoc Type</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(
                        f"<tr><td>{idoctyp}</td><td>{count}</td><td>{round(count/total_idocs*100, 2)}%</td></tr>"
                        for idoctyp, count in idoctyp_sorted
                    )}
                </tbody>
            </table>

            <h2>Processing Status</h2>
            <table>
                <thead>
                    <tr>
                        <th>Status Code</th>
                        <th>Description</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(
                        f"<tr><td>{status}</td><td>{get_status_description(status)}</td><td>{count}</td><td>{round(count/total_idocs*100, 2)}%</td></tr>"
                        for status, count in status_sorted
                    )}
                </tbody>
            </table>
    
            <h2>Direction Distribution</h2>
            <table>
                <thead>
                    <tr>
                        <th>Direction</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(
                        f"<tr><td>{direction}</td><td>{count}</td><td>{round(count/total_idocs*100, 2)}%</td></tr>"
                        for direction, count in direction_sorted
                    )}
                </tbody>
            </table>
    
            <h2>Daily Volume Trend</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(
                        f"<tr><td>{date}</td><td>{count}</td><td>{round(count/total_idocs*100, 2)}%</td></tr>"
                        for date, count in date_sorted
                    )}
                </tbody>
            </table>
    
            <h2>Partner Analysis</h2>
            <h3>Top Sending Partners</h3>
            {generate_partner_table(idoc_data, 'EDIDC_SNDPRN')}
    
            <h3>Top Receiving Partners</h3>
            {generate_partner_table(idoc_data, 'EDIDC_RCVPRN')}
    
            <div class="summary-card">
                <h3>Key Observations</h3>
                <ul>
                    <li>The most common message type is <span class="highlight">{mestyp_sorted[0][0] if mestyp_sorted else 'N/A'}</span> with {mestyp_sorted[0][1] if mestyp_sorted else 0} occurrences.</li>
                    <li>The majority of iDocs are <span class="highlight">{direction_sorted[0][0] if direction_sorted else 'N/A'}</span>.</li>
                    <li>The most frequent status is <span class="highlight">{status_sorted[0][0] if status_sorted else 'N/A'}</span> ({get_status_description(status_sorted[0][0]) if status_sorted else 'N/A'}).</li>
                </ul>
            </div>
        </body>
        </html>
    """
    
    return html

def generate_idoc_analytics2_text_report(idoc_data):
    """
    Generates a plain text analytics report from iDoc data (EDIDC and EDID4 combined records).
    
    Args:
        idoc_data (list): List of dictionaries containing iDoc records
        
    Returns:
        str: Plain text report string
    """
    if not idoc_data:
        return "No iDoc Data Available"
    
    # Reuse statistics calculations from the HTML version
    total_idocs = len(idoc_data)
    
    # Message type distribution
    mestyp_dist = {}
    idoctyp_dist = {}
    status_dist = {}
    direction_dist = {}
    date_dist = {}
    
    for record in idoc_data:
        # EDIDC fields
        mestyp = record.get('EDIDC_MESTYP', 'UNKNOWN')
        mestyp_dist[mestyp] = mestyp_dist.get(mestyp, 0) + 1
        
        idoctyp = record.get('EDIDC_IDOCTP', 'UNKNOWN')
        idoctyp_dist[idoctyp] = idoctyp_dist.get(idoctyp, 0) + 1
        
        status = record.get('EDIDC_STATUS', 'UNKNOWN')
        status_dist[status] = status_dist.get(status, 0) + 1
        
        direction = record.get('EDIDC_DIRECT', 'UNKNOWN')
        direction = "Outbound" if direction == "2" else "Inbound" if direction == "1" else direction
        direction_dist[direction] = direction_dist.get(direction, 0) + 1
        
        credat = record.get('EDIDC_CREDAT', 'UNKNOWN')
        date_dist[credat] = date_dist.get(credat, 0) + 1
    
    # Sort distributions by count
    mestyp_sorted = sorted(mestyp_dist.items(), key=lambda x: x[1], reverse=True)
    idoctyp_sorted = sorted(idoctyp_dist.items(), key=lambda x: x[1], reverse=True)
    status_sorted = sorted(status_dist.items(), key=lambda x: x[1], reverse=True)
    direction_sorted = sorted(direction_dist.items(), key=lambda x: x[1], reverse=True)
    date_sorted = sorted(date_dist.items(), key=lambda x: x[0], reverse=True)
    
    # Generate text report
    report = []
    report.append("="*70)
    report.append(f"iDoc Processing Analytics Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*70)
    report.append("")
    
    # Summary Overview
    report.append("SUMMARY OVERVIEW")
    report.append("-"*50)
    report.append(f"Total iDocs processed: {total_idocs}")
    report.append(f"Date range: {date_sorted[-1][0] if date_sorted else 'N/A'} to {date_sorted[0][0] if date_sorted else 'N/A'}")
    report.append("")
    
    # Message Type Distribution
    report.append("MESSAGE TYPE DISTRIBUTION")
    report.append("-"*50)
    for mestyp, count in mestyp_sorted:
        report.append(f"{mestyp:<20}: {count:>5} ({count/total_idocs*100:.2f}%)")
    report.append("")
    
    # iDoc Type Distribution
    report.append("IDOC TYPE DISTRIBUTION")
    report.append("-"*50)
    for idoctyp, count in idoctyp_sorted:
        report.append(f"{idoctyp:<20}: {count:>5} ({count/total_idocs*100:.2f}%)")
    report.append("")
    
    # Processing Status
    report.append("PROCESSING STATUS")
    report.append("-"*50)
    for status, count in status_sorted:
        report.append(f"{status:<5} - {get_status_description(status):<40}: {count:>5} ({count/total_idocs*100:.2f}%)")
    report.append("")
    
    # Direction Distribution
    report.append("DIRECTION DISTRIBUTION")
    report.append("-"*50)
    for direction, count in direction_sorted:
        report.append(f"{direction:<10}: {count:>5} ({count/total_idocs*100:.2f}%)")
    report.append("")
    
    # Daily Volume Trend
    report.append("DAILY VOLUME TREND")
    report.append("-"*50)
    for date, count in date_sorted:
        report.append(f"{date}: {count:>5} ({count/total_idocs*100:.2f}%)")
    report.append("")
    
    # Partner Analysis
    report.append("PARTNER ANALYSIS")
    report.append("-"*50)
    
    # Top Sending Partners
    report.append("Top Sending Partners:")
    send_partner_dist = {}
    for record in idoc_data:
        partner = record.get('EDIDC_SNDPRN', 'UNKNOWN')
        send_partner_dist[partner] = send_partner_dist.get(partner, 0) + 1
    send_partner_sorted = sorted(send_partner_dist.items(), key=lambda x: x[1], reverse=True)[:5]
    for partner, count in send_partner_sorted:
        report.append(f"  {partner:<30}: {count:>5}")
    report.append("")
    
    # Top Receiving Partners
    report.append("Top Receiving Partners:")
    recv_partner_dist = {}
    for record in idoc_data:
        partner = record.get('EDIDC_RCVPRN', 'UNKNOWN')
        recv_partner_dist[partner] = recv_partner_dist.get(partner, 0) + 1
    recv_partner_sorted = sorted(recv_partner_dist.items(), key=lambda x: x[1], reverse=True)[:5]
    for partner, count in recv_partner_sorted:
        report.append(f"  {partner:<30}: {count:>5}")
    report.append("")
    
    # Key Observations
    report.append("KEY OBSERVATIONS")
    report.append("-"*50)
    report.append(f"- The most common message type is {mestyp_sorted[0][0] if mestyp_sorted else 'N/A'} with {mestyp_sorted[0][1] if mestyp_sorted else 0} occurrences")
    report.append(f"- The majority of iDocs are {direction_sorted[0][0] if direction_sorted else 'N/A'}")
    report.append(f"- The most frequent status is {status_sorted[0][0] if status_sorted else 'N/A'} ({get_status_description(status_sorted[0][0]) if status_sorted else 'N/A'})")
    
    return "\n".join(report)

def generate_partner_table(idoc_data, partner_field):
    """Generate HTML table for partner analysis"""
    partner_dist = {}
    for record in idoc_data:
        partner = record.get(partner_field, 'UNKNOWN')
        partner_dist[partner] = partner_dist.get(partner, 0) + 1
    
    partner_sorted = sorted(partner_dist.items(), key=lambda x: x[1], reverse=True)[:10]  # Top 10
    
    return f"""
    <table>
        <thead>
            <tr>
                <th>Partner</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            {"".join(
                f"<tr><td>{partner}</td><td>{count}</td></tr>"
                for partner, count in partner_sorted
            )}
        </tbody>
    </table>
    """

def get_status_description(status_code):
    """Map status codes to human-readable descriptions"""
    status_map = {
        "03": "Data passed to application",
        "30": "IDoc ready for dispatch (ALE)",
        "53": "Application document posted",
        "68": "IDoc ready for dispatch (ALE)",
        "12": "Error in data",
        "29": "IDoc was edited",
    }
    return status_map.get(status_code, "Unknown status")

