<div align="center">
	<br/>
	<br/>
  <h1>
	<img height="140" src="assets/alma-cdk-domain.svg" alt="Alma CDK Domain" />
  <br/>
  <br/>
  </h1>

```sh
npm i -D @alma-cdk/domain
```

  <div align="left">

Simplifies creation of subdomain with a TLS certificate and configuration with services like AWS CloudFront.

  </div>
  <br/>
</div><br/>

## 🚧   Project Stability

![experimental](https://img.shields.io/badge/stability-experimental-yellow)

This construct is still versioned with `v0` major version and breaking changes might be introduced if necessary (without a major version bump), though we aim to keep the API as stable as possible (even within `v0` development). We aim to publish `v1.0.0` soon and after that breaking changes will be introduced via major version bumps.

<br/>

## Getting Started

```python
import { Domain } from '@alma-cdk/domain';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
```

```python
const domain = new Domain(this, 'Domain', {
  zone: 'example.com', // retrieve the zone via lookup, or provide IHostedZone
  subdomain: 'foobar', // optional subdomain
});

const distribution = new cloudfront.Distribution(this, 'Distribution', {
  /* other cloudfront configuration values removed for brevity */

  certificate: domain.certificate, // reference to created ICertificate
  domainNames: [domain.fqdn], // foobar.example.com
  enableIpv6: domain.enableIpv6, // true by default – set enableIpv6 prop to false during new Domain()
})

// assign CloudFront distribution to given fqdn with A + AAAA records
domain.addTarget(new targets.CloudFrontTarget(distribution))
```

<br/>

### CloudFront helper

Instead of assigning `certificate`, `domainNames` and `enableIpv6` properties individually, you may choose to use the one-liner helper utility method `configureCloudFront()` to set all three values at once – don't forget to use `...` object spread syntax:

```python
const distribution = new cloudfront.Distribution(this, 'Distribution', {
  /* other cloudfront configuration values removed for brevity */

  // one-liner to configure certificate, domainNames and IPv6 support
  ...domain.configureCloudFront(),
})

// assign CloudFront distribution to given fqdn with A + AAAA records
domain.addTarget(new targets.CloudFrontTarget(distribution))
```

Note: The returned domain names configuration is `domainNames: [domain.fqdn]`, meaning this only works in scenarios where your CloudFront distribution has only single domain name.
