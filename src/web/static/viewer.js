var osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay("view", {
    autoResize: true, // just an example for an option, no option is necessary.
    backend: "svg",
    drawTitle: true,
    // put further options here
  });

var load = function(file_location) {
  osmd
    .load(file_location)
    .then(() => osmd.render())
}


load("/notes/f6bac45d-c0e1-4101-ac5d-366dc1a9fa0c.musicxml")