const { PROPERTY_IDS } = require("../mock");
const { faker } = require("@faker-js/faker");

Array.prototype.sample = function () {
    return this[Math.floor(Math.random() * this.length)];
};

const OS = [
    "Android 6.0",
    "Android 12.0",
    "iOS 10",
    "iOS 15",
    "Windows OS",
    "Blackberry",
    "Windows",
    "OSX",
    "Ubuntu",
    "CentOS",
];
const CPU = [
    "Intel Core i7",
    "AMD Ryzen 4900X",
    "abi: armeabi-v7a ARMv7 Processor rev 4 (v7l)",
    "Qualcomm Snapdragon",
    "Samsung Exynos",
    "Apple M1",
];

const MAKE = [
    "Motorola XT1706",
    "Blackberry",
    "iPhone",
    "Google Pixel 7",
    "Samsung S23",
    "Windows Phone",
];

const BROWSERS = [
    "Chrome",
    "Mozilla Firefox",
    "Netscape Navigator",
    "Opera",
    "Microsoft Edge",
    "Safari",
];

faker.setLocale("en_IND");
const getDeviceData = (size) => {
    const DEVICE_IDS = PROPERTY_IDS("device", size);

    return DEVICE_IDS.map((device) => {
        const state = faker.address.state();
        const city = faker.address.city();
        const county = faker.address.county();
        return {
            fcm_token: "",
            city: city,
            device_id: device,
            device_spec: `"{'os':'${OS.sample()}','cpu':'${CPU.sample()}','make':'${MAKE.sample()}'}"`,
            state: state,
            uaspec: {
                agent: BROWSERS.sample(),
                ver: "76.0.3809.132",
                system: OS.sample(),
                raw: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            },
            country: "India",
            country_code: "IN",
            producer_id: "dev.obsrv.portal",
            state_code_custom: 29,
            state_code: `${state.substring(0, 2).toUpperCase()}`,
            state_custom: "Karnataka",
            district_custom: "Karnataka,s",
            first_access: 1568379184000,
            api_last_updated_on: 1568377184000,
            user_declared_district: county,
            user_declared_state: state,
        };
    });
};

module.exports = { getDeviceData };
