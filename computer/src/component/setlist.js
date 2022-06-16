import React, { useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableRow, Dialog, DialogActions, DialogTitle, DialogContent, Button } from "@mui/material";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import EdgesensorHighIcon from "@mui/icons-material/EdgesensorHigh";
import GavelIcon from "@mui/icons-material/Gavel";
import ContentPasteGoIcon from "@mui/icons-material/ContentPasteGo";

import Title from "./title";
import { TASK } from "../constant";

export default (props) => {
    const sendData = props["sendData"];
    const list = [
        { icon: <RestartAltIcon />, operation: "Reset", discription: "Reset the bed to sleepable position.", func: reset },
        {
            icon: <EdgesensorHighIcon />,
            operation: "Vibrate",
            discription: "Shake the bed!",
            func: () => {
                send("1");
            },
        },
        {
            icon: <GavelIcon />,
            operation: "Hammer",
            discription: "Hammer the sleepy person!",
            func: () => {
                send("2");
            },
        },
        {
            icon: <ContentPasteGoIcon />,
            operation: "Dump",
            discription: "Dump the person off the bed!",
            func: () => {
                send("3");
            },
        },
    ];
    const reset = () => {
        sendData(TASK.RESET);
    };
    const send = (state) => {
        sendData(TASK.SEND, state);
    };

    return (
        <React.Fragment>
            <Title>Settings</Title>
            <Table size="medium">
                <TableHead>
                    <TableCell>Operation</TableCell>
                    <TableCell>Discription</TableCell>
                </TableHead>
                <TableBody>
                    {list.map((item) => (
                        <TableRow>
                            <TableCell>
                                <Button variant="outlined" startIcon={item["icon"]} onClick={item["func"]}>
                                    {item["operation"]}
                                </Button>
                            </TableCell>
                            <TableCell>{item["discription"]}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </React.Fragment>
    );
};
