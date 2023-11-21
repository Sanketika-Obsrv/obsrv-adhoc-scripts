const fs = require('fs');
const path = require('path');

const scrapModules = (folderPath, basename) => {
    const mapping = new Map();
    fs.readdirSync(folderPath)
        .filter((file) => file !== basename)
        .map((file) => {
            const { eid, ...others } = require(path.join(folderPath, file))
            mapping.set(eid, others);
        });

    return mapping;
};

module.exports = { scrapModules }
