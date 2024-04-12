const zlib = require("zlib");
const fs = require("fs");

const compressFile = async (path, fileName) => {
    const handleStream = fs.createReadStream(path)
    return new Promise((resolve, reject) => {
        handleStream
            .pipe(zlib.createGzip())
            .pipe(fs.createWriteStream(`./output-test/${fileName}.gz`))
            .on('finish', () => {
                console.log(`Compression process done: ${fileName}`)
                resolve()
            }).on('error', (error) => {
                console.log(`Compression process failed: ${fileName}`)
                reject(error)
            })
    })
}; 

(async () => {
    try {
        console.log("Start")
        let data = fs.readdirSync(`./output-3`)
        for (let file of data) {
            await compressFile(`./output-3/${file}`, file)
        }
    }
    catch (error) {
        console.log(error)
    }
    finally {
        console.log("Exiting")
        process.exit()
    }
})()
