from kubernetes import client, config
import time
import requests

config.load_incluster_config()

custom = client.CustomObjectsApi()
core = client.CoreV1Api()
apps = client.AppsV1Api()

namespace = "default"

while True:
    sites = custom.list_namespaced_custom_object(
        group="stable.dwk",
        version="v1",
        namespace=namespace,
        plural="dummysites"
    )

    for site in sites["items"]:
        name = site["metadata"]["name"]
        url = site["spec"]["website_url"]

        print("Creating:", name)

        html = requests.get(url).text

        cm = client.V1ConfigMap(
            metadata=client.V1ObjectMeta(
                name=name + "-html"
            ),
            data={"index.html": html}
        )

        try:
            core.create_namespaced_config_map(namespace, cm)
        except:
            pass

        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=name + "-web"),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(
                    match_labels={"app": name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={"app": name}
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="nginx",
                                image="nginx:alpine",
                                volume_mounts=[
                                    client.V1VolumeMount(
                                        name="html",
                                        mount_path="/usr/share/nginx/html"
                                    )
                                ]
                            )
                        ],
                        volumes=[
                            client.V1Volume(
                                name="html",
                                config_map=client.V1ConfigMapVolumeSource(
                                    name=name + "-html"
                                )
                            )
                        ]
                    )
                )
            )
        )

        try:
            apps.create_namespaced_deployment(namespace, deployment)
        except:
            pass

        service = client.V1Service(
            metadata=client.V1ObjectMeta(name=name + "-service"),
            spec=client.V1ServiceSpec(
                selector={"app": name},
                ports=[client.V1ServicePort(port=80, target_port=80)]
            )
        )

        try:
            core.create_namespaced_service(namespace, service)
        except:
            pass

    time.sleep(5)