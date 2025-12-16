# Q1

```
docker@ubuntusrv:/app/machine-learning-zoomcamp/cohorts/2025/05-deployment/homework$ python3 q6_test.py
{'conversion_probability': 0.49999999999842815, 'conversion': False}
```

# Q2

```
docker@ubuntusrv:~$ kind --version
kind version 0.30.0
docker@ubuntusrv:~$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:38279
CoreDNS is running at https://127.0.0.1:38279/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

# Q3 & Q4

```
docker@ubuntusrv:~$ kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
subscription-568c5d8cf-qsdxj   1/1     Running   0          22m
docker@ubuntusrv:~$ kubectl get svc
NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes             ClusterIP      10.96.0.1      <none>        443/TCP        38m
subscription-service   LoadBalancer   10.96.91.186   <pending>     80:31732/TCP   19m
docker@ubuntusrv:~$ kubectl get deployment
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
subscription   1/1     1            1           22m

# Q6

```
docker@ubuntusrv:~$ cat deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subscription
spec:
  selector:
    matchLabels:
      app: subscription
  replicas: 1
  template:
    metadata:
      labels:
        app: subscription
    spec:
      containers:
      - name: subscription
        image: zoomcamp-model:3.13.10-hw10
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        ports:
        - containerPort: 9696
```

# Q7

```
docker@ubuntusrv:~$ cat service.yaml
apiVersion: v1
kind: Service
metadata:
  name: subscription-service
spec:
  type: LoadBalancer
  selector:
    app: subscription
  ports:
  - port: 80
    targetPort: 9696

```

# Testing the service

```
docker@ubuntusrv:~$ kubectl port-forward service/subscription-service 9696:80
Forwarding from 127.0.0.1:9696 -> 9696
Handling connection for 9696

docker@ubuntusrv:/app/machine-learning-zoomcamp/cohorts/2025/05-deployment/homework$ python3 q6_test.py
{'conversion_probability': 0.49999999999842815, 'conversion': False}
```

# Autoscaling

```
docker@ubuntusrv:~$ kubectl get hpa
NAME               REFERENCE                 TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
subscription-hpa   Deployment/subscription   cpu: 2%/20%   1         3         1          19m
```