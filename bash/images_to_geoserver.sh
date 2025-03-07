kubectl exec -it geoserver-pod-0 -- /bin/bash

wget -q https://dl.min.io/client/mc/release/linux-amd64/mc -O /tmp/mc 
chmod +x /tmp/mc 

export MC_HOST_s3=

/tmp/mc find s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/ \
    --name "*.tif" --path "*/2021/250/*" \
    | xargs -I {} /tmp/mc cp {} /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021/
chmod -R a+rw /opt/geoserver/data_dir