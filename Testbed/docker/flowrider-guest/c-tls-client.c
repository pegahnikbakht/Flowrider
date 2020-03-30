/* From https://wiki.openssl.org/index.php/SSL/TLS_Client */

#define HOST_NAME "www.random.org"
#define HOST_PORT "443"
#define HOST_RESOURCE "/cgi-bin/randbyte?nbytes=32&format=h"

long res = 1;

SSL_CTX* ctx = NULL;
BIO *web = NULL, *out = NULL;
SSL *ssl = NULL;

init_openssl_library();

const SSL_METHOD* method = SSLv23_method();
if(!(NULL != method)) handleFailure();

ctx = SSL_CTX_new(method);
if(!(ctx != NULL)) handleFailure();

/* Cannot fail ??? */
SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, verify_callback);

/* Cannot fail ??? */
SSL_CTX_set_verify_depth(ctx, 4);

/* Cannot fail ??? */
const long flags = SSL_OP_NO_SSLv2 | SSL_OP_NO_SSLv3 | SSL_OP_NO_COMPRESSION;
SSL_CTX_set_options(ctx, flags);

res = SSL_CTX_load_verify_locations(ctx, "random-org-chain.pem", NULL);
if(!(1 == res)) handleFailure();

web = BIO_new_ssl_connect(ctx);
if(!(web != NULL)) handleFailure();

res = BIO_set_conn_hostname(web, HOST_NAME ":" HOST_PORT);
if(!(1 == res)) handleFailure();

BIO_get_ssl(web, &ssl);
if(!(ssl != NULL)) handleFailure();

const char* const PREFERRED_CIPHERS = "HIGH:!aNULL:!kRSA:!PSK:!SRP:!MD5:!RC4";
res = SSL_set_cipher_list(ssl, PREFERRED_CIPHERS);
if(!(1 == res)) handleFailure();

res = SSL_set_tlsext_host_name(ssl, HOST_NAME);
if(!(1 == res)) handleFailure();

out = BIO_new_fp(stdout, BIO_NOCLOSE);
if(!(NULL != out)) handleFailure();

res = BIO_do_connect(web);
if(!(1 == res)) handleFailure();

res = BIO_do_handshake(web);
if(!(1 == res)) handleFailure();

/* Step 1: verify a server certificate was presented during the negotiation */
X509* cert = SSL_get_peer_certificate(ssl);
if(cert) { X509_free(cert); } /* Free immediately */
if(NULL == cert) handleFailure();

/* Step 2: verify the result of chain verification */
/* Verification performed according to RFC 4158    */
res = SSL_get_verify_result(ssl);
if(!(X509_V_OK == res)) handleFailure();

/* Step 3: hostname verification */
/* An exercise left to the reader */

BIO_puts(web, "GET " HOST_RESOURCE " HTTP/1.1\r\n"
              "Host: " HOST_NAME "\r\n"
              "Connection: close\r\n\r\n");
BIO_puts(out, "\n");

int len = 0;
do
{
  char buff[1536] = {};
  len = BIO_read(web, buff, sizeof(buff));

  if(len > 0)
    BIO_write(out, buff, len);

} while (len > 0 || BIO_should_retry(web));

if(out)
  BIO_free(out);

if(web != NULL)
  BIO_free_all(web);

if(NULL != ctx)
  SSL_CTX_free(ctx);
