/* This example code is placed in the public domain. */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <gnutls/gnutls.h>
#include <gnutls/x509.h>

/* A very basic TLS client, with X.509 authentication and server certificate
 * verification. Note that error recovery is minimal for simplicity.
 */

 //#define SERVER_IP "172.31.1.2"
 #define SERVER_IP "127.0.0.1"
 // The TCP port number that the server is running on, which we will connect to.
 #define SERVER_PORT 50556

#define CHECK(x) assert((x)>=0)
#define LOOP_CHECK(rval, cmd) \
        do { \
                rval = cmd; \
        } while(rval == GNUTLS_E_AGAIN || rval == GNUTLS_E_INTERRUPTED); \
        assert(rval >= 0)

#define MAX_BUF 1024
#define MSG "GET / HTTP/1.0\r\n\r\n"

extern void tcp_close(int sd);

int main(void)
{
        int ret, sd, ii;
        gnutls_session_t session;
        char buffer[MAX_BUF + 1], *desc;
        gnutls_datum_t out;
        int type;
        unsigned status;
        gnutls_certificate_credentials_t xcred;

        if (gnutls_check_version("3.4.6") == NULL) {
                fprintf(stderr, "GnuTLS 3.4.6 or later is required for this example\n");
                exit(1);
        }

        /* for backwards compatibility with gnutls < 3.3.0 */
        CHECK(gnutls_global_init());

        /* X509 stuff */
        CHECK(gnutls_certificate_allocate_credentials(&xcred));

        /* sets the system trusted CAs for Internet PKI */
        CHECK(gnutls_certificate_set_x509_system_trust(xcred));

        /* If client holds a certificate it can be set using the following:
         *
         gnutls_certificate_set_x509_key_file (xcred, "cert.pem", "key.pem",
         GNUTLS_X509_FMT_PEM);
         */

        /* Initialize TLS session */
        CHECK(gnutls_init(&session, GNUTLS_CLIENT));

        CHECK(gnutls_server_name_set(session, GNUTLS_NAME_DNS, "www.example.com",
                                     strlen("www.example.com")));

        /* It is recommended to use the default priorities */
        CHECK(gnutls_set_default_priority(session));

        /* put the x509 credentials to the current session
         */
        CHECK(gnutls_credentials_set(session, GNUTLS_CRD_CERTIFICATE, xcred));
        gnutls_session_set_verify_cert(session, "www.example.com", 0);

        /* connect to the peer
         */
         int connfd = make_one_connection(SERVER_IP, SERVER_PORT);
         int *connfdPtr = malloc(sizeof(int));
         *connfdPtr = connfd;

//        gnutls_transport_set_int(session, connfdPtr);

        gnutls_transport_set_ptr(session, connfdPtr);
        // Set the callback that allows GnuTLS to PUSH data TO the transport layer
        gnutls_transport_set_push_function(session, data_push);
        // Set the callback that allows GnuTls to PULL data FROM the tranport layer
        gnutls_transport_set_pull_function(session, data_pull);

//        gnutls_handshake_set_timeout(session,
//                                     GNUTLS_DEFAULT_HANDSHAKE_TIMEOUT);

        /* Perform the TLS handshake
         */
        do {
                ret = gnutls_handshake(session);
        }
        while (ret < 0 && gnutls_error_is_fatal(ret) == 0);
        if (ret < 0) {
                if (ret == GNUTLS_E_CERTIFICATE_VERIFICATION_ERROR) {
                        /* check certificate verification status */
                        type = gnutls_certificate_type_get(session);
                        status = gnutls_session_get_verify_cert_status(session);
                        CHECK(gnutls_certificate_verification_status_print(status,
                              type, &out, 0));
                        printf("cert verify output: %s\n", out.data);
                        gnutls_free(out.data);
                }
                fprintf(stderr, "*** Handshake failed: %s\n", gnutls_strerror(ret));
                goto end;
        } else {
                desc = gnutls_session_get_desc(session);
                printf("- Session info: %s\n", desc);
                gnutls_free(desc);
        }

        // If the handshake worked, we can now receive the data that the server is
        // sending to us.
        //printf("------- BEGIN DATA FROM SERVER -------\n");
        char buf[100];
        res = gnutls_record_recv(session, buf, sizeof(buf));
        while (res != 0) {
            if (res == GNUTLS_E_REHANDSHAKE) {
                error_exit("Peer wants to re-handshake but we don't support that.\n");
            } else if (gnutls_error_is_fatal(res)) {
                error_exit("Fatal error during read.\n");
            } else if (res > 0) {
               // fwrite(buf, 1, res, stdout);
                fflush(stdout);
            }
            res = gnutls_record_recv(session, buf, sizeof(buf));
        }
        //printf("------- END DATA FROM SERVER -------\n");


        CHECK(gnutls_bye(session, GNUTLS_SHUT_RDWR));

      end:

        // Destroy the session.
        gnutls_deinit(session);

        // Close the TCP connection.
        close(connfd);

        gnutls_certificate_free_credentials(xcred);

        gnutls_global_deinit();

        return 0;
}
