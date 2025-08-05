import speedtest

def get_network_speed():
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        return (
            f"Ping: {st.results.ping:.2f} ms\n"
            f"Download speed: {st.results.download / 1_000_000:.2f} Mbps\n"
            f"Upload speed: {st.results.upload / 1_000_000:.2f} Mbps"
        )
    except Exception as e:
        return f"Speedtest failed: {str(e)}"
