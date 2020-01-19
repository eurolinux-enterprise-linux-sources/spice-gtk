#include <stdint.h>

#ifndef _H_TEST_MARSHALLERS

typedef struct {
    uint32_t data_size;
    uint8_t dummy_byte;
    uint64_t *data;
} SpiceMsgMainShortDataSubMarshall;

typedef struct {
    int8_t *name;
} SpiceMsgMainArrayMessage;

#endif /* _H_TEST_MARSHALLERS */

