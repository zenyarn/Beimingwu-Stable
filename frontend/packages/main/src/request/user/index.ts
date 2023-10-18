import { checkedFetch, useProgressedFetch } from "../utils";
import { getSemanticSpecification } from "../engine";
import { Learnware, Response } from "types";

const BASE_URL = "./api/user";

function getProfile(): Promise<{
  code: number;
  msg: string;
  data: {
    username: string;
    email: string;
  };
}> {
  return checkedFetch(`${BASE_URL}/profile`, {
    method: "POST",
  }).then((res) => res.json());
}

function changePassword({
  oldPasswordMd5,
  newPasswordMd5,
}: {
  oldPasswordMd5: string;
  newPasswordMd5: string;
}): Promise<{ code: number; msg: string }> {
  return checkedFetch(`${BASE_URL}/change_password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      old_password: oldPasswordMd5,
      new_password: newPasswordMd5,
    }),
  }).then((res) => res.json());
}

function deleteLearnware({ id }: { id: string }): Promise<{
  code: number;
  msg: string;
}> {
  return checkedFetch(`${BASE_URL}/delete_learnware`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      learnware_id: id,
    }),
  }).then((res) => res.json());
}

function getLearnwareList({ page, limit }: { page: number; limit: number }): Promise<{
  code: number;
  msg: string;
  data: {
    learnware_list: Response.LearnwareDetailInfo[];
    page: number;
    limit: number;
    total_pages: number;
  };
}> {
  return checkedFetch(`${BASE_URL}/list_learnware`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      page,
      limit,
    }),
  }).then((res) => res.json());
}

function addLearnware({
  edit = false,
  name,
  dataType,
  taskType,
  libraryType,
  tagList,
  dataTypeDescription,
  taskTypeDescription,
  description,
  files,
  learnwareId,
  onProgress,
}: {
  edit?: boolean;
  name: Learnware.Name;
  dataType: Learnware.DataType;
  taskType: Learnware.TaskType;
  libraryType: Learnware.LibraryType;
  tagList: Learnware.TagList;
  dataTypeDescription: string;
  taskTypeDescription: string;
  description: Learnware.Description;
  files: Learnware.Files;
  learnwareId: string;
  onProgress: (progress: number) => void;
}): Promise<{ code: number; msg: string }> {
  const { progressedFetch } = useProgressedFetch(onProgress);

  return getSemanticSpecification()
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = name;
      semanticSpec.Data.Values = (dataType && [dataType]) || [];
      semanticSpec.Task.Values = (taskType && [taskType]) || [];
      semanticSpec.Library.Values = (libraryType && [libraryType]) || [];
      semanticSpec.Scenario.Values = tagList;
      semanticSpec.Description.Values = description;
      semanticSpec.Input = JSON.parse(dataTypeDescription);
      semanticSpec.Output = JSON.parse(taskTypeDescription);

      const fd = new FormData();
      fd.append("learnware_file", files[0].size === 0 ? "" : files[0]);
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      edit && learnwareId && fd.append("learnware_id", learnwareId);
      return fd;
    })
    .then((fd) =>
      edit
        ? progressedFetch(`${BASE_URL}/update_learnware`, {
            method: "POST",
            body: fd,
          })
        : progressedFetch(`${BASE_URL}/add_learnware`, {
            method: "POST",
            body: fd,
          }),
    )
    .then((res) => res.json());
}

function verifyLog({ learnware_id }: { learnware_id: string }): Promise<{ data: string }> {
  return checkedFetch(`${BASE_URL}/verify_log?learnware_id=${learnware_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

function createToken(): Promise<{
  code: number;
  msg: string;
}> {
  return checkedFetch(`${BASE_URL}/create_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

function listToken(): Promise<{
  code: number;
  msg: string;
  data: {
    token_list: string[];
  };
}> {
  return checkedFetch(`${BASE_URL}/list_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

function deleteToken({ token }: { token: string }): Promise<{
  code: number;
  msg: string;
}> {
  return checkedFetch(`${BASE_URL}/delete_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: token,
    }),
  }).then((res) => res.json());
}

export {
  getProfile,
  changePassword,
  deleteLearnware,
  getLearnwareList,
  addLearnware,
  verifyLog,
  createToken,
  listToken,
  deleteToken,
};
