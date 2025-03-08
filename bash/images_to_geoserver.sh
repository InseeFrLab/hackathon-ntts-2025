kubectl exec -it geoserver-pod-0 -- /bin/bash

wget -q https://dl.min.io/client/mc/release/linux-amd64/mc -O /tmp/mc 
chmod +x /tmp/mc 

export MC_HOST_s3=


/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BE100/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BE251/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FRK26/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FRJ27/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/HR050/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/ITI32/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/RO123/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FI1C1/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/UKJ22/2024/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/

/tmp/mc rm /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/filename2bbox.parquet 
/tmp/mc rm /opt/geoserver/data_dir/SENTINEL2/NUTS3/2024-new/metrics-normalization.yaml


/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BE100/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BE251/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FRK26/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FRJ27/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/HR050/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/ITI32/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/RO123/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FI1C1/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/PL414/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/ES612/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/LU000/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/CY000/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/IE061/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/EE00A/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/SI035/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BG322/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/SK022/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/DEA54/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/CZ072/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/DK041/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/EL521/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/LV008/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/LT028/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/UKJ22/2021/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/

/tmp/mc rm /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/filename2bbox.parquet 
/tmp/mc rm /opt/geoserver/data_dir/SENTINEL2/NUTS3/2021-new/metrics-normalization.yaml


/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BE100/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BE251/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FRK26/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FRJ27/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/HR050/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/ITI32/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/RO123/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/FI1C1/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/PL414/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/ES612/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/LU000/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/CY000/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/IE061/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/EE00A/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/SI035/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/BG322/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/SK022/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/DEA54/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/CZ072/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/DK041/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/EL521/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/LV008/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/LT028/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/
/tmp/mc cp -r s3/projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/UKJ22/2018/250/ /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/


/tmp/mc rm /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/filename2bbox.parquet 
/tmp/mc rm /opt/geoserver/data_dir/SENTINEL2/NUTS3/2018-new/metrics-normalization.yaml


chmod -R a+rw /opt/geoserver/data_dir