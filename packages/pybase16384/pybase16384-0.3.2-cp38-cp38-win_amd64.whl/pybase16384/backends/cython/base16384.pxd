# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport int32_t


cdef extern from "base16384.h" nogil:
    ctypedef enum base16384_err_t:
        base16384_err_ok
        base16384_err_get_file_size
        base16384_err_fopen_output_file
        base16384_err_fopen_input_file
        base16384_err_write_file
        base16384_err_open_input_file
        base16384_err_map_input_file
    # encode_len calc min buf size to fill encode result
    int b14_encode_len "base16384_encode_len" (int dlen)
# decode_len calc min buf size to fill decode result
    int b14_decode_len "base16384_decode_len" (int dlen, int offset)

# encode data and write result into buf
    int b14_encode "base16384_encode" (const char* data, int dlen, char* buf, int blen)
# decode data and write result into buf
    int b14_decode "base16384_decode" (const char* data, int dlen, char* buf, int blen)

    base16384_err_t b14_encode_file "base16384_encode_file" (const char * input, const char * output, char * encbuf, char * decbuf)
    base16384_err_t b14_decode_file "base16384_decode_file" (const char * input, const char * output, char * encbuf, char * decbuf)

cdef extern from * nogil:
    """
#ifdef CPUBIT32
#define pybase16384_64bits() 0
#else
#define pybase16384_64bits() 1
#endif
    """
    int32_t pybase16384_64bits()
