
### ds2 model (~387MB):
https://drive.google.com/open?id=0B_s7AwBOnuD-ckRqQWM3WFctZmM

### sample audio files:

Please upload your samples audio to HDFS. For instance, hdfs://127.0.0.1:9001/deepspeech/data

Please save your ds2.model to HDFS. For instance, hdfs://127.0.0.1:9001/deepspeech/data/ds2.model

### run on clusters

```shell
./bigdl.sh -- spark-submit --master local[1] \
--conf spark.driver.memory=20g \
--conf "spark.serializer=org.apache.spark.serializer.JavaSerializer" \
--class com.intel.analytics.zoo.pipeline.deepspeech2.example.InferenceEvaluate \
pipeline-0.1-SNAPSHOT-jar-with-dependencies.jar \
--host hdfs://127.0.0.1:9001 --path /deepspeech/data
```