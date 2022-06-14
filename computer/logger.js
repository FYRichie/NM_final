class Logger {
    info = (msg) => {
        console.log(`[Info] ${msg}`);
    };
    success = (msg) => {
        console.log(`[Success] ${msg}`);
    };
    error = (msg) => {
        console.log(`[Error] ${msg}`);
    };
}

module.exports = Logger;
