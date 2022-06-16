import React, { useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableRow, Dialog, DialogActions, DialogTitle, DialogContent, Button } from "@mui/material";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { ClockPicker } from "@mui/x-date-pickers/ClockPicker";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add";

import Title from "./title";
import { TASK } from "../constant";

export default (props) => {
    const sendData = props["sendData"];
    const timelist = props["timelist"];

    const [openadd, setOpenadd] = useState(false);
    const [openchange, setOpenchange] = useState(false);
    const [addtime, setAddtime] = useState(new Date());
    const [targettime, setTargettime] = useState(new Date());
    const [sourcetime, setSourcetime] = useState(new Date());

    const deleteTime = (time) => {
        sendData(TASK.DELETE_TIME, time);
    };
    const changeTime = () => {
        sendData(TASK.CHANGE_TIME, {
            source_time: date2str(sourcetime),
            target_time: date2str(targettime),
        });
        setOpenchange(false);
    };
    const addTime = () => {
        sendData(TASK.ADD_TIME, date2str(addtime));
        closeAdd();
    };
    const openAdd = () => {
        setOpenadd(true);
    };
    const closeAdd = () => {
        setOpenadd(false);
        setAddtime(new Date());
    };
    const openChange = (time) => {
        setOpenchange(true);
        setTargettime(time);
        setSourcetime(time);
    };
    const closeChange = () => {
        setOpenchange(false);
        setTargettime(new Date());
        setSourcetime(new Date());
    };
    const changeActivate = (time) => {
        sendData(TASK.CHANGE_ACTIVATE, time);
    };
    const str2date = (time) => {
        const date = new Date();
        const time_slice = time.split(":");
        date.setHours(parseInt(time_slice[0]));
        date.setMinutes(parseInt(time_slice[1]));
        return date;
    };
    const date2str = (date) => {
        return date.getHours() + ":" + date.getMinutes();
    };

    return (
        <React.Fragment>
            <Title>Alarm Clocks</Title>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>Time</TableCell>
                        <TableCell>Activate</TableCell>
                        <TableCell></TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {timelist.map((item) => (
                        <TableRow>
                            <TableCell
                                onClick={() => {
                                    openChange(str2date(item["time"]));
                                }}>
                                {item["time"]}
                            </TableCell>
                            <TableCell
                                onClick={() => {
                                    changeActivate(item["time"]);
                                }}>
                                {item["activate"] ? <CheckIcon /> : <CloseIcon />}
                            </TableCell>
                            <TableCell>
                                <DeleteIcon
                                    onClick={() => {
                                        console.log("Delete: ", item["time"]);
                                        deleteTime(item["time"]);
                                    }}
                                />
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                <Button variant="outlined" startIcon={<AddIcon />} onClick={openAdd}>
                    Add clock
                </Button>
            </Table>
            {/* Add time */}
            <Dialog open={openadd}>
                <DialogTitle>Add an alarm clock</DialogTitle>
                <DialogContent>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <ClockPicker
                            date={addtime}
                            onChange={(newTime) => {
                                setAddtime(newTime);
                            }}
                        />
                    </LocalizationProvider>
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeAdd}>Cancel</Button>
                    <Button onClick={addTime}>Ok</Button>
                </DialogActions>
            </Dialog>
            {/* Change time */}
            <Dialog open={openchange}>
                <DialogTitle>Change the alarm clock</DialogTitle>
                <DialogContent>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <ClockPicker
                            date={sourcetime}
                            onChange={(newTime) => {
                                setSourcetime(newTime);
                            }}
                        />
                    </LocalizationProvider>
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeChange}>Cancel</Button>
                    <Button onClick={changeTime}>Ok</Button>
                </DialogActions>
            </Dialog>
        </React.Fragment>
    );
};
