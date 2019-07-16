source bin/activate
cd SuperNova
export PYTHONPATH=/home/shelly/flask/star/star/SuperNova/index/caffe-fast-rcnn/python
export PYTHONPATH=/home/shelly/flask/star/star/SuperNova/index:${PYTHONPATH}
python manage.py runserver 0.0.0.0:8009