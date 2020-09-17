>     174. Describe and give an example of each of the following types of polymorphism:
>
> * Ad-hoc polymorphism
> * Parametric polymorphism
> * Subtype polymorphism

**Parametric polymorphism:** Say we have some list of items; this could be a list of integers, doubles, strings, 
whatever. Now consider a method `head()` that returns the first item from that list. This method doesn't care if the 
item is of type Int, String, Apple or Orange. Its return type is the one list is parameterized with and its 
implementation is the same for all types: "return first item".

Unlike parametric polymorphism, **Ad-hoc polymorphism** is bound to a type. Depending on the type, different 
implementations of the method are invoked. Method overloading is one example of ad-hoc polymorphism. For example, 
we can have two versions of method that appends two items - one that takes two integers and adds them, and one that 
takes two strings and concatenates them. You know, 2 plus 3 is 5, but "2" plus "3" is "23".

There's also a third kind of polymorphism, **Subtyping polymorphism**, in which subclasses provide different 
implementations of some superclass method. Unlike the ad-hoc polymorphism where the decision on which implementation 
is being invoked is made at compile time, in subtyping polymorphism it is made at run time (in case of parametric 
polymorphism there is just one implementation so no decision is being made there).

See [Ad-hoc polymorphism and type classes](https://medium.com/@sinisalouc/ad-hoc-polymorphism-and-type-classes-442ae22e5342).

>     183. Describe what happens when you type a URL into your browser and press Enter.

1. User types `somedomain.com` into the address bar of their browser.

2. The browser checks various caches for a DNS record to find the corresponding IP address of `somedomain.com`.
    1. System hosts file, `/etc/hosts` on Linux, `%SystemRoot%\System32\drivers\etc\hosts` on Windows.
    2. Browser cache.
    3. OS cache.
    4. Router cache.
    5. ISP DNS server cache.

3. If the requested URL is not in any of the caches, ISP’s DNS server initiates a DNS query to find the IP address of 
   the server that hosts `somedomain.com`.
   
   The purpose of a DNS query is to search multiple DNS servers on the internet until it finds the correct IP address 
   for the website. This type of search is called a recursive search since the search will repeatedly continue from a 
   DNS server to a DNS server until it either finds the IP address or returns an error response saying it was 
   unable to find it.
   
   Many website URLs we encounter today contain a third-level domain, a second-level domain, and a top-level domain. 
   Each of these levels contains their own name server, which is queried during the DNS lookup process.
   
   For `somedomain.com`, first, the DNS recursor will contact the root name server. The root name server will redirect 
   it to the `.com` domain name server. `.com` name server will redirect it to the `somedomain.com` name server. 
   The `somedomain.com` name server will find the matching IP address in its DNS records and return it to the DNS 
   recursor, which will send it back to the browser.
   
   These requests are sent using small data packets that contain information such as the content of the request and 
   the IP address it is destined for (IP address of the DNS recursor). These packets travel through multiple networking 
   equipment between the client and the server before it reaches the correct DNS server. These equipments use routing 
   tables to figure out the fastest possible way for the packet to reach its destination. If these packets 
   get lost, the user gets a request failed error. Otherwise, they reach the correct DNS server, grab the correct 
   IP address, and come back to the browser.
   
4. The browser initiates a TCP connection with the server.

   TCP/IP three-way handshake:
    1. The client machine sends a `SYN` packet to the server over the internet, asking if it is open for new 
    connections.
    2. If the server has open ports that can accept and initiate new connections, it responds with an `ACK`nowledgment 
    of the `SYN` packet using a `SYN/ACK` packet.
    3. The client receives the `SYN/ACK` packet from the server and acknowledges it by sending an `ACK` packet.
    
   A TCP connection has been successfully established.
   
5. The browser sends an HTTP request to the webserver.

   This request also contains additional information such as browser identification (`User-Agent`), 
   types of responses that it will accept (`Accept`), and connection headers asking it to keep the TCP 
   connection alive for additional requests. It also passes information taken from cookies the browser has in store 
   for this domain.

6. The server handles the request and sends back a response.

   The server response contains the web page requested for as well as the status code, compression type (`Content-Encoding`), 
   how to cache the page (`Cache-Control`), any cookies to set, privacy information, etc.
   
7. The browser displays the HTML content.

   The browser displays the HTML content in phases. First, it renders the bare bone HTML skeleton. Then it checks the 
   HTML tags and send out `GET` requests for additional elements on the web page, such as images, CSS stylesheets, 
   JavaScript files, etc. These static files are cached by the browser, so that it doesn't have to fetch them again 
   the next time the page is visited.
   
   In the end, `somedomain.com` appears on the browser.

>     Describe client-server SSL communication.

TLS is an encryption protocol designed to secure Internet communications. A TLS handshake is the process that kicks off 
a communication session that uses TLS encryption. During a TLS handshake, the two communicating sides exchange messages 
to acknowledge each other, verify each other, establish the encryption algorithms they will use, and agree on session 
keys. TLS handshakes are a foundational part of how HTTPS works.

**TLS vs. SSL handshakes**

SSL, or Secure Sockets Layer, was the original encryption protocol developed for HTTP. SSL was replaced by TLS, or 
Transport Layer Security, some time ago. SSL handshakes are now called TLS handshakes, although the "SSL" name is still 
in wide use.

**When does a TLS handshake occur?**

A TLS handshake takes place whenever a user navigates to a website over HTTPS and the browser first begins to query 
the website's [origin server](https://www.cloudflare.com/learning/cdn/glossary/origin-server/). A TLS handshake also 
happens whenever any other communications use HTTPS, including API calls and DNS over HTTPS queries.

TLS handshakes occur after a TCP connection has been opened via a TCP handshake.

**What happens during a TLS handshake?**

During the course of a TLS handshake, the client and server together will do the following:

* Specify which version of TLS (TLS 1.0, 1.2, 1.3, etc.) they will use.
* Decide on which cipher suites (see below) they will use.
* Authenticate the identity of the server via the server’s public key and the SSL certificate authority’s digital 
signature.
* Generate session keys in order to use symmetric encryption after the handshake is complete.

**What are the steps of a TLS handshake?**

TLS handshakes are a series of datagrams, or messages, exchanged by a client and a server. A TLS handshake involves 
multiple steps, as the client and server exchange the information necessary for completing the handshake and making 
further conversation possible.

The exact steps within a TLS handshake will vary depending upon the kind of key exchange algorithm used and the cipher 
suites supported by both sides. The RSA key exchange algorithm is used most often. It goes as follows:

1. The 'client hello' message: The client initiates the handshake by sending a "hello" message to the server. The 
message will include which TLS version the client supports, the cipher suites supported, and a string of random bytes 
known as the "client random."
2. The 'server hello' message: In reply to the client hello message, the server sends a message containing the server's 
SSL certificate, the server's chosen cipher suite, and the "server random," another random string of bytes that's 
generated by the server.
3. Authentication: The client verifies the server's SSL certificate with the certificate authority that issued it. This 
confirms that the server is who it says it is, and that the client is interacting with the actual owner of the domain.
4. The premaster secret: The client sends one more random string of bytes, the "premaster secret." The premaster secret 
is encrypted with the public key and can only be decrypted with the private key by the server. (The client gets the 
public key from the server's SSL certificate.)
5. Private key used: The server decrypts the premaster secret.
6. Session keys created: Both client and server generate session keys from the client random, the server random, and 
the premaster secret. They should arrive at the same results.
7. Client is ready: The client sends a "finished" message that is encrypted with a session key.
8. Server is ready: The server sends a "finished" message encrypted with a session key.
9. Secure symmetric encryption achieved: The handshake is completed, and communication continues using the session keys.

**What is a cipher suite?**

A cipher suite is a set of encryption algorithms for use in establishing a secure communications connection. 
(An encryption algorithm is a set of mathematical operations performed on data for making data appear random.) There 
are a number of cipher suites in wide use, and an essential part of the TLS handshake is agreeing upon which cipher 
suite will be used for that handshake.

> Difference Between a Java Keystore and a Truststore

In most cases, we use a keystore and a truststore when our application needs to communicate over SSL/TLS.
Usually, these are password-protected files that sit on the same file system as our running application. The default 
format used for these files is JKS until Java 8. Since Java 9, though, the default keystore format is PKCS12. 
The biggest difference between JKS and PKCS12 is that JKS is a format specific to Java, while PKCS12 is a 
standardized and language-neutral way of storing encrypted private keys and certificates.

**Java KeyStore**

A Java keystore stores private key entries, certificates with public keys or just secret keys that we may use for 
various cryptographic purposes. It stores each by an alias for ease of lookup.

Generally speaking, keystores hold keys that our application owns that we can use to prove the integrity of a message 
and the authenticity of the sender, say by signing payloads.

Usually, we'll use a keystore when we are a server and want to use HTTPS. During an SSL handshake, the server looks up 
the private key from the keystore and presents its corresponding public key and certificate to the client.

Correspondingly, if the client also needs to authenticate itself – a situation called mutual authentication – then the
 client also has a keystore and also presents its public key and certificate.

There's no default keystore, so if we want to use an encrypted channel, we'll have to set `javax.net.ssl.keyStore` and 
`javax.net.ssl.keyStorePassword`. If our keystore format is different than the default, we could use 
`javax.net.ssl.keyStoreType` to customize it.

Of course, we can use these keys to service other needs as well. Private keys can sign or decrypt data, and public keys 
can verify or encrypt data. Secret keys can perform these functions as well. A keystore is a place that we can hold 
onto these keys.

**Java TrustStore**

In Java, we use it to trust the third party we're about to communicate with.

Take our earlier example. If a client talks to a Java-based server over HTTPS, the server will look up the associated 
key from its keystore and present the public key and certificate to the client.

We, the client, then look up the associated certificate in our truststore. If the certificate or Certificate Authorities 
presented by the external server is not in our truststore, we'll get an `SSLHandshakeException` and the connection 
won't be set up successfully.

Java has bundled a truststore called `cacerts` and it resides in the `$JAVA_HOME/jre/lib/security directory`.

Here, we can override the default truststore location via the `javax.net.ssl.trustStore` property. Similarly, we can 
set `javax.net.ssl.trustStorePassword` and `javax.net.ssl.trustStoreType` to specify the truststore's password and type.
