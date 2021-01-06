const path = require("path");
const fs = require("fs");
const uuid = require("uuid");
const NYC = require("nyc");

const NYC_OUTPUT_DIR = ".nyc_output";
const NYC_MERGE_DIR = path.join(NYC_OUTPUT_DIR, "merge");

module.exports = {
  cleanMergeFiles: async () => {
    // Run once before all tests
    if (fs.existsSync(NYC_MERGE_DIR)) {
      fs.rmdirSync(NYC_MERGE_DIR, { recursive: true }, (err) => {});
    }
    if (fs.existsSync(NYC_OUTPUT_DIR)) {
      await fs.promises.mkdir(NYC_MERGE_DIR);
    }
  },
  captureNycCoverage: async (page) => {
    if (fs.existsSync(NYC_OUTPUT_DIR)) {
      var coverage = await page.evaluate(`window.__coverage__`);
      if (!coverage) {
        console.error("Coverage could not be evaluated!");
      } else {
        if (!fs.existsSync(NYC_MERGE_DIR)) {
          await fs.promises.mkdir(NYC_MERGE_DIR);
        }
        await fs.promises.writeFile(
          path.join(NYC_MERGE_DIR, `${uuid.v4()}.json`),
          JSON.stringify(coverage)
        );
      }
    }
  },
  mergeNycCoverage: async () => {
    if (fs.existsSync(NYC_OUTPUT_DIR) && fs.existsSync(NYC_MERGE_DIR)) {
      const nyc = new NYC({});
      const map = await nyc.getCoverageMapFromAllCoverageFiles(NYC_MERGE_DIR);
      const outputFile = path.join(NYC_OUTPUT_DIR, "coverage.json");
      const content = JSON.stringify(map, null, 2);
      await fs.promises.writeFile(outputFile, content);
    }
  },
};
