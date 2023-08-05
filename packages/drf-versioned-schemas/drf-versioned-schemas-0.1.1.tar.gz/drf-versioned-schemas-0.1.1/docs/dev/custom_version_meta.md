# 模型类增加自定义`VersionMeta`

由于Django的Model类限制Meta传参未定义字段，抛出如下异常。

```python
>>> TypeError: 'class Meta' got invalid attribute(s)
```

为了非侵入地解决这个问题，我们采取自定义一个新的Meta类实现我们需要的功能。

暂时把逻辑转移到序列化类实现（序列化类无此限制），后续根据实际情况决定。


## 参考资料
   
- https://stackoverflow.com/questions/1088431/adding-attributes-into-django-models-meta-class