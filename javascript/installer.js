// GitHub API URL to list contents of the 'manifests' directory
const apiUrl = 'https://api.github.com/repos/FutureProofHomes/Documentation/contents/manifests';

// Function to fetch releases dynamically
async function fetchReleases() {
  try {
    const releasesResponse = await fetch(apiUrl);
    const releases = await releasesResponse.json();
    /* console.log('Fetched releases:', releases); */

    for (const release of releases) {
      if (release.type === 'dir') { // Only process directories if needed
        fetchManifestFromRelease(release);
      }
    }

  } catch (error) {
    console.error('Error fetching Releases:', error);
  }
}

// Function to fetch all manifests associated with a release
async function fetchManifestFromRelease(release) {
	try {
    const manifestResponse = await fetch(release.url); // Fetch using the 'url' from each item
    const manifests = await manifestResponse.json();
    console.log(`Manifests for ${release.name}:`, manifests);
		
    populateManifestVersions(release, manifests);
    
  } catch (error) {
    console.error(`Error fetching manifest for ${release.name}:`, error);
  }
}

// Function to add all manifest versions to drop down
function populateManifestVersions(release, manifests) {
	const versionSelect = document.getElementById('version-select');
  
  manifests.forEach(manifest => {
  	console.log(manifest);
    const option = document.createElement('option');
    option.value = manifest.download_url;
    option.textContent = release.name;
    versionSelect.appendChild(option);
  });
}


// Update the manifest URL based on selections
function updateManifestURL() {
  const version = document.getElementById('version-select').value;
  console.log(version);

  if (version.includes("alpha") || version.includes("beta")) {
    document.getElementById('warning').style.display = 'block';
  }
  else {
    document.getElementById('warning').style.display = 'none';
  }

  // Update the manifest attribute
  document.getElementById('install-button').setAttribute('manifest', version);
}

// Initialize the form
document.addEventListener('DOMContentLoaded', () => {
  fetchReleases();

  // Add event listeners
  document.querySelectorAll('input[name="revision"]').forEach(radio => {
    radio.addEventListener('change', updateManifestURL);
  });
  document.getElementById('version-select').addEventListener('change', updateManifestURL);
});