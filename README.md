\## DBaaS vs DIY PostgreSQL



\### DBaaS (Google Cloud SQL)



Pros:

\- Faster to initialize because Google manages the database infrastructure.

\- Automated maintenance and updates are handled by the cloud provider.

\- Backups are easier to configure and manage.

\- High availability and scaling options are available.

\- Less work is needed for database administration.



Cons:

\- Has ongoing cloud costs.

\- Requires a billing-enabled Google Cloud project.

\- Less control over the underlying database infrastructure.

\- Costs can increase with storage, traffic and database resources.



\### DIY PostgreSQL with Kubernetes



Pros:

\- More control over the PostgreSQL configuration and deployment.

\- Can be run using our existing Kubernetes cluster and PersistentVolumes.

\- No separate managed database service is required.

\- Useful for learning Kubernetes stateful applications.



Cons:

\- More work is required to initialize and maintain PostgreSQL.

\- We are responsible for upgrades, monitoring and troubleshooting.

\- Backups must be configured and maintained ourselves.

\- Storage and backup failures must be handled by us.

\- Running the database still consumes cluster resources.



\### Summary



DBaaS reduces maintenance work and makes backups and operations easier, but it has cloud costs. DIY PostgreSQL gives more control and is useful for learning, but requires significantly more administration and backup work.

