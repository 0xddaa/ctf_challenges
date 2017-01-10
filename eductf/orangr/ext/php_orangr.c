#include <php.h>
#include <gmp.h>

#include "php_orangr.h"

int cmp[] = {0, 1, 2, 0, 3, 4, 5, 2, 2, 6, 3, 2, 5, 8, 10, 5, 4, 0, 8, 9, 3, 2, 21, 4, 10, 2, 13, 25, 25, 13, 24, 23, 5, 7, 28, 20, 19, 5, 31, 12, 13, 4, 16, 3, 2, 27, 19, 2, 32, 39, 17, 29, 28, 24, 6, 35};

zend_function_entry orangr_functions[] = {
    PHP_FE(check_user, NULL)
    PHP_FE(check_pw, NULL)
    { NULL, NULL, NULL }
};

zend_module_entry orangr_module_entry = {
    STANDARD_MODULE_HEADER,
    PHP_ORANGR_EXTNAME,
    orangr_functions,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    PHP_ORANGR_VERSION,
    STANDARD_MODULE_PROPERTIES
};

ZEND_GET_MODULE(orangr)

PHP_FUNCTION(check_user) {
    zval *zuser;
    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "z", &zuser) == FAILURE) {
        return;
    }

    char *user;
    user = Z_STRVAL_P(zuser);
    if (!strcmp(user, "pwn_gg")) {
        RETURN_TRUE;
    } else {
        RETURN_FALSE;
    }
}

PHP_FUNCTION(check_pw) {
    zval *zkey;
    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "z", &zkey) == FAILURE) {
        return;
    }

    char *key;
    mpz_t num;
    int cos[56];

    key = Z_STRVAL_P(zkey);
    mpz_init(num);
    mpz_set_str(num, key, 10);

    /* convert to coefficient array */
    for (int i = 0; mpz_cmp_ui(num, 0) > 0 && i < 56; i++) {
        cos[i] = mpz_fdiv_ui(num, 56);
        mpz_fdiv_q_ui(num, num, 56);
    }
    mpz_clear(num);

    int ret = 1;
    /* calculate compare array */
    for (int i = 0; i < 56; i++) {
        int count = 0;
        for (int j = 0; j < i; j++) {
            if (cos[j] > cos[i])
                count++;
        }
        if (count != cmp[i])
            RETURN_FALSE;
    }
    RETURN_TRUE;
}
