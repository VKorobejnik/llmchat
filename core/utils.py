import streamlit as st
import gc
import ctypes
import ctypes.util

def cleanup_memory():
    st.cache_data.clear()
    gc.collect()
    # Manually trigger Python's memory allocator to release blocks
    try:
        libc_path = ctypes.util.find_library('c')
        if libc_path is not None:
            print(f"Found C library")
            libc = ctypes.CDLL(libc_path)
            if hasattr(libc, 'malloc_trim'):
                libc.malloc_trim(0)  # Release memory to OS (Linux/glibc)
    except Exception as e:
        print(f"Could not release memory via malloc_trim: {e}")