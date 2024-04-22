Реферальная система
для доступа к api

{{url}}/user/auth_phone/
в дату кладется телефон
пример даты 
{"phone": "7900000001"}
в ответ приходит код

{{url}}/user/register/
пример даты 
{
    "auth_code": 7810,
    "first_name": "test",
    "last_name": "ya",
    "password": "1234"
}
 пример ответа
 {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMzkwNjg3OCwiaWF0IjoxNzEzODIwNDc4LCJqdGkiOiIzODRiYTMxMzY2Zjk0YzcyYjlhZjQ4MzBiNjhlMmZlYSIsInVzZXJfaWQiOjZ9.WRvu5EB-oxEeUYRtTgjySGLlGClCC9jr1ACLvuhZ5JY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzODIwNzc4LCJpYXQiOjE3MTM4MjA0NzgsImp0aSI6ImU4MjY3NjMwMzVkODQ4YWY4MmIzMDZhNzhhNzU5ZTQwIiwidXNlcl9pZCI6Nn0.s4OdqQWvzNtLISt2UACJBYAqsGn-JhSLqmCafCp86QU"
}

access нужно использовать при любом запросе к api

{{url}}/referral_system/get_referral_code/
пример ответа
{
    "referral_code": "29OS8b"
}
это реферальный код пользователя

метод put
{{url}}/referral_system/activate_referral_code/
активация реферального кода
пример даты 
{
    "code": "29OS8b"
}

