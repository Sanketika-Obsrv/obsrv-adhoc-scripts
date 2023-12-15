const path = require('path');
const { scrapModules } = require('../../utils/fs');

const eDataObjects = scrapModules(__dirname, path.basename(__filename));

const getEdata = eid => {
    const edataObject = eDataObjects.get(eid);
    if (!edataObject) return null;
    return edataObject.edata();
}

module.exports = { getEdata }