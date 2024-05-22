ARG PLATFORM_VERSION=latest

FROM jetbrains/qodana-jvm-community:$PLATFORM_VERSION

ARG JET_BRAINS_ACADEMY_PLUGIN=JetBrainsAcademy.zip
# ITP hardcoded course
ARG MARKETPLACE_COURSE_ID=16630

COPY $JET_BRAINS_ACADEMY_PLUGIN "/tmp/JetBrainsAcademy.zip"

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends unzip python3 && \
    unzip /tmp/JetBrainsAcademy.zip && \
    mkdir /opt/plugins && mv JetBrainsAcademy /opt/plugins/ && \
    apt-get purge --auto-remove -y unzip && \
    rm -rf /var/cache/apt /var/lib/apt/ /tmp/*

# Language settings
ENV COM_JETBRAINS_EDU_PROJECT_PYTHON_INTERPRETER="/usr/bin/python3"

RUN $QODANA_DIST/bin/idea.sh installCoursePlugins --marketplace $MARKETPLACE_COURSE_ID -Dplugin.path=/opt/plugins/JetBrainsAcademy -Djava.awt.headless=true

ENTRYPOINT ["/opt/idea/bin/idea.sh", "validateCourse", "/project/data", "--marketplace=16630", "--tests=true", "--links=true", "-Dplugin.path=/opt/plugins/JetBrainsAcademy", "-Djava.awt.headless=true"]
