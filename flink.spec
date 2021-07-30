%define __jar_repack %{nil}

%global debug_package %{nil}

# Use local caches compile
%global compile_for_local 0

%global with_debug 0

%global with_tests 0

Name:           flink
Version:        1.12.0
Release:        4
Summary:        Stateful Computations over Data Streams
License:        Apache License v2.0
URL:            https://github.com/apache/%{name}
Source0:        https://github.com/apache/%{name}/archive/release-%{version}.tar.gz
Source1:        settings.xml
Source2:        https://packages.confluent.io/maven/io/confluent/kafka-schema-registry-client/5.5.2/kafka-schema-registry-client-5.5.2.jar
Source3:        https://packages.confluent.io/maven/io/confluent/kafka-avro-serializer/5.5.2/kafka-avro-serializer-5.5.2.jar
Source4:        https://packages.confluent.io/maven/io/confluent/kafka-schema-serializer/5.5.2/kafka-schema-serializer-5.5.2.jar

Patch0:         0001-add-npm.hw-repo.patch
Patch1:         0002-fix-compilation-failure.patch
BuildRequires:  java-1.8.0-openjdk-devel maven
Requires:       java-1.8.0-openjdk

%description
Apache Flink is a framework and distributed processing engine for stateful computations over unbounded and bounded data streams. Flink has been designed to run in all common cluster environments, perform computations at in-memory speed and at any scale.


%prep
%autosetup -p1 -n %{name}-release-%{version}
mvn install:install-file -DgroupId=io.confluent -DartifactId=kafka-schema-registry-client -Dversion=5.5.2 -Dpackaging=jar -Dfile=%{SOURCE2}
mvn install:install-file -DgroupId=io.confluent -DartifactId=kafka-avro-serializer -Dversion=5.5.2 -Dpackaging=jar -Dfile=%{SOURCE3}
mvn install:install-file -DgroupId=io.confluent -DartifactId=kafka-schema-serializer -Dversion=5.5.2 -Dpackaging=jar -Dfile=%{SOURCE4}
%build

maven_cmd="clean package " 

%if 0%{?compile_for_local}
 cp  %{SOURCE1} ./
 maven_cmd="${maven_cmd} -s settings.xml"
%endif

%if 0%{?with_debug}
 maven_cmd="${maven_cmd} -X "
%endif

%if 0%{?with_tests:1}
 maven_cmd="${maven_cmd} -DskipTests"
%endif

mvn ${maven_cmd}

%install
mkdir -p %{buildroot}/opt/
cp -rf ../%{name}-release-%{version}/flink-dist/target/%{name}-%{version}-bin/%{name}-%{version} %{buildroot}/opt/apache-%{name}-%{version}

find %{buildroot}/opt/apache-%{name}-%{version}/ -type f -name '*.py' | xargs -i sed -i 's/\#!\/usr\/bin\/env python$/\#!\/usr\/bin\/python3/' {}

%files
/opt/apache-%{name}-%{version}
%doc README.md
%license LICENSE

%changelog
* Wed Jul 21 2021 zhangjiapeng <zhangjiapeng@huawei.com> - 1.12.0-4
- Fix compilation failure.

* Wed Dec 23 2020 weidong <weidong@uniontech.com> - 1.12.0-3
- Add npm.huawei repo.

* Thu Dec 17 2020 weidong <weidong@uniontech.com> - 1.12.0-2
- Fix compilation issues.

* Mon Dec 14 2020 weidong <weidong@uniontech.com> - 1.12.0-1
- Initial package.
