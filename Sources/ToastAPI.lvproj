<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="26008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">26.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str">LabVIEW 2026 Windows toast wrapper: direct composition and display through ToastBuilder, activation registration through ToastService, and an injected ActivationHandler for copied arguments and user-input values. Includes an interactive text-reply example. See README.md and CALLBACK-LIFETIME.md for ownership, shutdown and current limits.</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Examples" Type="Folder">
			<Item Name="Build Toast With Classes.vi" Type="VI" URL="../Examples/Build Toast With Classes.vi"/>
			<Item Name="Native Toast Example.vi" Type="VI" URL="../Examples/Native Toast Example.vi"/>
		</Item>
		<Item Name="Support" Type="Folder">
			<Item Name="Merge Release Error.vi" Type="VI" URL="../Support/Merge Release Error.vi"/>
			<Item Name="Native Add Argument Integer.vi" Type="VI" URL="../Support/Native Add Argument Integer.vi"/>
			<Item Name="Native Button Add Argument.vi" Type="VI" URL="../Support/Native Button Add Argument.vi"/>
		</Item>
		<Item Name="ToastNotification.lvlib" Type="Library" URL="../ToastNotification/ToastNotification.lvlib"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
