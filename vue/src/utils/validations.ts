// 公共校验函数
export const isRequired = (rule, value, callback) => {
    if (!value) {
        callback(new Error('不能为空'));
    } else {
        callback();
    }
};

export const checkPassword = (rule, value, callback) => {
    if (value.length < 8) {
        callback(new Error('密码长度至少需要8位及以上'));
    } else {
        callback();
    }
};
export const checkEmail = (rule, value, callback) => {
    const emailReg = /^([a-zA-Z0-9._%-])+@([a-zA-Z0-9.-])+\.([a-zA-Z]{2,4})$/;
    if (!value) {
        callback(new Error('请输入邮箱地址'));
    } else if (!emailReg.test(String(value).toLowerCase())) {
        callback(new Error('邮箱地址不合法'));
    } else {
        callback();
    }
};

export const checkPhone = (rule, value, callback) => {
    const phoneRegex = /^1[3-9]\d{9}$/;
    if (value.length != 11) {
        callback(new Error('手机号码长度错误'));
    } else if (!phoneRegex.test(String(value))) {
        callback(new Error('手机号码不合法'));
    } else {
        callback();
    }
};

