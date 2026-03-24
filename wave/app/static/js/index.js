// RANGE <-> NUMBER SYNC

function setValueRangeNumber(idInRanger, idInNumber){
  document.getElementById(idInRanger).addEventListener("input", function () {
    document.getElementById(idInNumber).value = this.value;
  });
}

function setValueNumberRanger(idInNumber, idInRanger){
  document.getElementById(idInNumber).addEventListener("input", function () {
    document.getElementById(idInRanger).value = this.value;
  });
}

// Server
setValueRangeNumber("memoryserver", "memserverValue")
setValueNumberRanger("memserverValue","memoryserver")

setValueRangeNumber("vcpuserver", "cpuserverValue")
setValueNumberRanger("cpuserverValue","vcpuserver")

// Client
setValueRangeNumber("memoryclient", "memclientValue")
setValueNumberRanger("memclientValue","memoryclient")

setValueRangeNumber("vcpuclient", "cpuclientValue")
setValueNumberRanger("cpuclientValue","vcpuclient")


// MODEL SELECTION

document.getElementById("model-select").addEventListener("change", function() {
  const modelsParms = ['sin', 'flashc', 'step'];

  document.getElementById("err-msg").style.display = "none";
  document.getElementById("mb-field").style.display = "none";

  modelsParms.forEach((valor) => {
    document.getElementById(valor).style.display = "none";
  });

  let selectedDiv = document.getElementById(this.value);
  if(selectedDiv){
    selectedDiv.style.display = "flex";
    document.getElementById("mb-field").style.display = "block";
  }
});


// MODEL VALIDATION

document.querySelector("form").addEventListener("submit", function(e) {
  const errMsg = document.getElementById("err-msg");
  errMsg.style.display = "none";
  errMsg.innerText = "";

  const amplitude = parseFloat(document.getElementById("amplitude-sinusoid").value);
  const lambd = parseFloat(document.getElementById("lambd-sinusoid").value);

  if (document.getElementById("model-select").value === "sin" && amplitude >= lambd) {
    e.preventDefault();
    errMsg.style.display = "block";
    errMsg.innerText = "Amplitude must be less than lambda";
  }
});


// PLATFORM SELECTION

document.getElementById("docker-server").addEventListener("click", function() {
  document.querySelectorAll(".ram-cpu-fields").forEach((element) => {
    element.style.display = "none";
  });
});

document.getElementById("vm-server").addEventListener("click", function() {
  document.querySelectorAll(".ram-cpu-fields").forEach((element) => {
    element.style.display = "block";
  });
});

document.getElementById("docker").addEventListener("click", function() {
  document.querySelectorAll(".ram-cpu-fields-client").forEach((element) => {
    element.style.display = "none";
  });
});

document.getElementById("vm").addEventListener("click", function() {
  document.querySelectorAll(".ram-cpu-fields-client").forEach((element) => {
    element.style.display = "block";
  });
});


// TOPOLOGY TYPE (TREE / LINEAR)

document.addEventListener("DOMContentLoaded", function () {

  const topologySelect = document.getElementById("topology-type");
  const treeConfig = document.getElementById("tree-config");
  const linearConfig = document.getElementById("linear-config");
  const mininetFields = document.getElementById("mininet-config-fields");

  function toggleTopologyFields() {
    const selected = topologySelect.value;

    if (!selected) {
      mininetFields.classList.add("d-none");
      return;
    }

    mininetFields.classList.remove("d-none");

    treeConfig.classList.add("d-none");
    linearConfig.classList.add("d-none");

    if (selected === "tree")
      treeConfig.classList.remove("d-none");

    if (selected === "linear")
      linearConfig.classList.remove("d-none");

    updateLinks();
  }

  topologySelect.addEventListener("change", toggleTopologyFields);
  toggleTopologyFields();
});

// ==============================
// NETWORK MODE (DELAY / LOSS / BW)
// ==============================
const delayNone = document.getElementById("delay-none");
const delayGlobal = document.getElementById("delay-global");
const delaySpecific = document.getElementById("delay-specific");

const delayField = document.getElementById("delay-field");
const lossField = document.getElementById("loss-field");
const bwField = document.getElementById("bw-field"); // ✅ NOVO

const specificTable = document.getElementById("specific-delay-table");

function updateDelayMode() {

  if (delayNone.checked) {
    delayField.classList.add("d-none");
    lossField.classList.add("d-none");
    bwField.classList.add("d-none"); // ✅ NOVO
    specificTable.classList.add("d-none");
  }

  if (delayGlobal.checked) {
    delayField.classList.remove("d-none");
    lossField.classList.remove("d-none");
    bwField.classList.remove("d-none"); // ✅ NOVO
    specificTable.classList.add("d-none");
  }

  if (delaySpecific.checked) {
    delayField.classList.add("d-none");
    lossField.classList.add("d-none");
    bwField.classList.add("d-none"); // ✅ NOVO
    specificTable.classList.remove("d-none");
  }
}

delayNone.addEventListener("change", updateDelayMode);
delayGlobal.addEventListener("change", updateDelayMode);
delaySpecific.addEventListener("change", updateDelayMode);

// ==============================
// LINK TABLE GENERATION
// ==============================
const delayTableBody = document.getElementById("delay-table-body");

// -------- Tree calculadora --------
function calculateTreeSwitches(depth, branching) {
  if (branching === 1) return depth;
  return (Math.pow(branching, depth) - 1) / (branching - 1);
}

function generateTreeLinks(depth, branching, maxSwitches) {

  const realMax = Math.min(
    calculateTreeSwitches(depth, branching),
    maxSwitches
  );

  let links = [];
  let next = 2;

  function build(parent, level) {
    if (next > realMax || level >= depth) return;

    for (let i = 0; i < branching; i++) {
      if (next > realMax) break;

      links.push({
        src: `s${parent}`,
        dst: `s${next}`
      });

      const child = next;
      next++;
      build(child, level + 1);
    }
  }

  build(1, 1);
  return links;
}

// -------- LINEAR --------
function generateLinearLinks(n) {
  let links = [];

  for (let i = 1; i < n; i++) {
    links.push({
      src: `s${i}`,
      dst: `s${i+1}`
    });
  }

  return links;
}

// -------- POPULATE TABLE --------
function populateDelayTable(links) {
  delayTableBody.innerHTML = "";

  links.forEach(link => {
    const row = `
      <tr>
        <td>${link.src} ↔ ${link.dst}</td>
        <td><input type="number" name="delay_${link.src}_${link.dst}" class="form-control" min="0"></td>
        <td><input type="number" name="loss_${link.src}_${link.dst}" class="form-control" min="0" max="100"></td>
        <td><input type="number" name="bw_${link.src}_${link.dst}" class="form-control" min="0"></td> <!-- ✅ NOVO -->
      </tr>
    `;
    delayTableBody.insertAdjacentHTML("beforeend", row);
  });
}

// -------- UPDATE LINKS --------
function updateLinks() {

  const topology = document.getElementById("topology-type").value;

  if (topology === "tree") {

    const depth = parseInt(document.getElementById("depth").value);
    const branching = parseInt(document.getElementById("branching").value);
    const maxSwitches = parseInt(document.getElementById("switchs").value);

    if (!depth || !branching || !maxSwitches) return;

    const links = generateTreeLinks(depth, branching, maxSwitches);
    populateDelayTable(links);
  }

  if (topology === "linear") {

    const n = parseInt(document.getElementById("linear_switchs").value);
    if (!n) return;

    const links = generateLinearLinks(n);
    populateDelayTable(links);
  }
}

document.getElementById("depth").addEventListener("input", updateLinks);
document.getElementById("branching").addEventListener("input", updateLinks);
document.getElementById("switchs").addEventListener("input", updateLinks);
document.getElementById("linear_switchs").addEventListener("input", updateLinks);