function deleteNote(mId, code) {
    fetch("/delete-mess", {
      method: "POST",
      body: JSON.stringify({ mId: mId }),
    }).then((_res) => {
      window.location.href = "/chat/"+code;
    });
  }