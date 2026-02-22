const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const dropArea = document.getElementById("dropArea");
const submitBtn = document.getElementById("submitBtn");
const resultDiv = document.getElementById("result");

// ==============================
// Form Submit → Upload → Extract → Structure
// ==============================

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!fileInput.files.length) {
    resultDiv.innerHTML =
      '<p class="text-red-600 font-medium">Please select a PDF file first.</p>';
    return;
  }

  submitBtn.disabled = true;
  submitBtn.innerHTML =
    '<i class="fas fa-spinner fa-spin mr-2"></i> Processing...';

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    // ==========================
    // 1️⃣ Upload
    // ==========================
    const uploadResponse = await fetch("/api/extract-pdf", {
      method: "POST",
      body: formData,
    });

    const uploadData = await uploadResponse.json();
  

   if (!uploadResponse.ok) {
  throw new Error(uploadData.detail || "Upload failed");
}

console.log("Uploaded successfully:", uploadData.filename);
    const filename = uploadData.filename;

    // ==========================
    // 2️⃣ Extract Text
    // ==========================
    const extractResponse = await fetch(`/extract-text/${filename}`, {
      method: "POST",
    });

    const extractData = await extractResponse.json();

    if (!extractResponse.ok) {
      throw new Error(extractData.detail || "Extraction failed");
    }

    // ==========================
    // 3️⃣ Structured Report
    // ==========================
    const structureResponse = await fetch(`/structure-report/${filename}`, {
      method: "POST",
    });

    const structureData = await structureResponse.json();

    if (!structureResponse.ok) {
      throw new Error(structureData.detail || "Structuring failed");
    }

    const structuredData = structureData.structured_data;

    // Save to localStorage (optional)
    localStorage.setItem("extracted_text", extractData.text);
    localStorage.setItem(
      "structured_data",
      JSON.stringify(structuredData)
    );

    // ==========================
    // 4️⃣ Build Structured Table
    // ==========================

    let rows = "";
    // If no structured data → stop here
if (!structuredData || structuredData.length === 0) {
  resultDiv.innerHTML = `
    <p class="text-red-600 font-medium mt-4">
      Invalid or unrelated medical report. Please upload a proper lab report.
    </p>
  `;  
  return;
}

    if (structuredData.length > 0) {
      structuredData.forEach((test) => {
        let statusColor =
          test.status === "High"
            ? "text-red-600"
            : test.status === "Low"
            ? "text-yellow-600"
            : test.status === "Normal"
            ? "text-green-600"
            : "text-gray-600";

        rows += `
          <tr class="border-b">
                
            <td class="p-2 font-medium">${test.test_name}</td>
            <td class="p-2">${test.value}</td>
            <td class="p-2">${test.unit}</td>
            <td class="p-2">${test.normal_range}</td>
            <td class="p-2 font-bold ${statusColor}">
              ${test.status}
            </td>
          </tr>
        `;
      });
    } else {
      rows = `
        <tr>
          <td colspan="5" class="p-4 text-center text-gray-500">
            No lab values detected in report.
          </td>
        </tr>
      `;
    }

    // ==========================
    // 5️⃣ Display Everything
    // ==========================

    resultDiv.innerHTML = `
      <div class="bg-green-50 border border-green-200 rounded-lg p-6 mt-6">

        <h3 class="text-lg font-bold mb-3">
          Extracted Text Preview
        </h3>
        <pre class="whitespace-pre-wrap text-sm bg-white p-4 rounded border max-h-60 overflow-auto">
${extractData.text.substring(0, 1500)}
        </pre>

        <h3 class="text-lg font-bold mt-6 mb-3">
          Structured Medical Report
        </h3>

        <div class="overflow-x-auto">
          <table class="min-w-full text-sm text-left border bg-white">
            <thead class="bg-gray-100">
              <tr>
                <th class="p-2">Test Name</th>
                <th class="p-2">Value</th>
                <th class="p-2">Unit</th>
                <th class="p-2">Normal Range</th>
                <th class="p-2">Status</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
            </tbody>
          </table>
        </div>

        <button onclick="window.location.href='/patient-context'" 
                class="mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
          Go to Patient Context →
        </button>
      </div>
    `;
  } catch (err) {
    resultDiv.innerHTML = `
      <p class="text-red-600 mt-4">
        Error: ${err.message}
      </p>
    `;
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = "Analyze Report";
  }
});