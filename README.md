# Scrapy with Frontera 
Scrapy + Frontera (A crawling project) - translated from the original Japanese version. (Thanks RY-2718)

## Dependencies:
- [Scrapy](https://github.com/scrapy/scrapy)
- [Frontera](https://github.com/scrapinghub/frontera)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache HBase](https://hbase.apache.org/)
- [Twisted Python](https://twistedmatrix.com/trac/)
    - docs/twisted-change.md (Change according to this instructions)

## Introduction
### Python package dependencies
virtualenv - Please do not do it unless you separate the environment with etc.
Solve dependencies for distibuted / kafka / hbase, then uninstall and install via the master.

```
$ pip install scrapy colorlog msgpack-python frontera[distributed,kafka,hbase]
$ pip uninstall frontera
$ pip install pip install git+https://github.com/scrapinghub/frontera.git
```

### Edit the Configuration File
Settings for scrapy's behavior are '/crawler/settings.py'.
Frontera's settings are '/frontier/common.py', '/frontier/*_settings.py'.
logging settings are in 'logging.conf'

The items to be set at a minimum are listed below.

#### /crawler/settings.py
```
BUCKET_NAME # S3[Bucket name]
```

#### /frontier/common.py
```
SPIDER_FEED_PARTITIONS # number of spiders(Scrapy) 
SPIDER_LOG_PARTITIONS #  number of workers(Frontera)

KAFKA_LOCATION # Kafka location: e.g., 'localhost:9092'
# Settings related to kafka:
# All is fine as long as it matches between Scrapy and Frontera, but it seems reasonable to slightly change the default name.
SPIDER_LOG_DBW_GROUP
SPIDER_LOG_SW_GROUP
SCORING_LOG_DBW_GROUP
SPIDER_FEED_GROUP
SPIDER_LOG_TOPIC
SPIDER_FEED_TOPIC
SCORING_LOG_TOPIC
```

#### /frontier/\*\_settings.py
```
HBASE_THRIFT_HOST = 'localhost' # HBase location
HBASE_THRIFT_PORT = 9090 # Port number where HBase's Thrift client runs, default is 9090
HBASE_METADATA_TABLE = 'metadata' # The table name created by Frontera. If it is not created, Frontera creates it automatically.
HBASE_QUEUE_TABLE = 'queue' # The table name created by Frontera. If it is not created, Frontera creates it automatically.
```

### Kafka, HBase settings
Introduce Kafka, create a topic (match `SPIDER_LOG_TOPIC, SPIDER_FEED_TOPIC, SCORING_LOG_TOPIC` above).

An example command is shown below. For details, please refer to [kafka document](https://kafka.apache.org/documentation/#quickstart).
```
$ /path/to/kafka/bin/kafka-topics.sh --create --topic frontier-done --replication-factor 1 --partitions 1 --zookeeper localhost:2181
$ /path/to/kafka/bin/kafka-topics.sh --create --topic frontier-score --replication-factor 1 --partitions 1 --zookeeper localhost:2181
$ /path/to/kafka/bin/kafka-topics.sh --create --topic frontier-todo --replication-factor 1 --partitions 2 --zookeeper localhost:2181
```

Also, introduce HBase and create a namespace called `crawler`.

An example command is shown below. For details, refer to [HBase document](https://hbase.apache.org/book.html#_namespace).```
$ hbase shell
> create_namespace 'crawler'
```

How to move
### Frontera
It is assumed that Kafka + zookeeper is running.

Launch two terminals and start each worker of frontera. It restarts every time frontera's worker terminates in `run _ *. sh`..

```
$ cd /path/to/project/root
$ bash scripts/run_db.sh
```
```
$ cd /path/to/project/root
$ bash scripts/run_strategy.sh
```

At the time of termination, we terminate frontera as follows. I try to hit a script to stop frontera's loop.
```
$ cd /path/to/project/root
$ bash scripts/kill_frontera_loop.sh
```

### Scrapy
It is assumed that frontera worker is running.

#### First Time Setup
Create `partition_id.txt` in the project root as follows and execute 'scripts/init.sh'.
The number now is the ID of Scrapy managed by Frontera.
In this example, the ID of Scrapy is 0.

```
$ cd /path/to/project/root
$ echo 0 > partition_id.txt
$ bash scripts/init.sh
```

#### Procedure for starting Scrapy
Launch the terminal as many as Scrapy and start Scrapy. Like frontera, it restarts every time Scrapy finishes in a shell script.
```
$ cd /path/to/project/root
$ bash scripts/loop_scrapy.sh
```

Scrapyのログは `scrapy_log/scrapy.log` に吐き出されます．pythonのloggingモジュールによってローテーションがかかることがあるので，監視する場合は `tail -F` を使うと良いと思います．

```
$ tail -F ~/workspace/frontera7/japanese_company_spider[0,1]/scrapy_log/scrapy.log
```
