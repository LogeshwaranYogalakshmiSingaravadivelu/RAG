FROM liquibase/liquibase:latest

# Copy from local liquibase/ directory into container
COPY ./changelog /liquibase/db/changelog
COPY ./liquibase.properties /liquibase/liquibase.properties

WORKDIR /liquibase

ENTRYPOINT ["liquibase"]
CMD ["--changeLogFile=db/changelog/db.changelog-master.yaml", "update"]
