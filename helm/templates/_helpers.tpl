{{/*
Expand the name of the chart.
*/}}
{{- define "machina.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "machina.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "machina.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "machina.labels" -}}
helm.sh/chart: {{ include "machina.chart" . }}
{{ include "machina.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Pod labels
*/}}
{{- define "machina.podLabels" -}}
{{- range $key, $val := .Values.config.podLabels -}}
{{ $key }}: {{ $val | quote }}
{{ end -}}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "machina.selectorLabels" -}}
app.kubernetes.io/name: {{ include "machina.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "machina.llmserver.selectorLabels" -}}
{{ include "machina.selectorLabels" .}}
app: llm-server-v2
{{- end }}


{{/*
Create the name of the service account to use
*/}}
{{- define "machina.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "machina.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "machina.adminServiceAccountName" -}}
{{- if .Values.adminServiceAccount.create }}
{{- default (printf "%s-admin" (include "machina.fullname" .) ) .Values.adminServiceAccount.name }}
{{- else }}
{{- default "default" .Values.adminServiceAccount.name }}
{{- end }}
{{- end }}


{{- define "machina.llmserver.image" -}}
{{- if .Values.imageRepository -}}
{{ .Values.imageRepository }}/{{ .Values.components.llmserver.image }}:{{ .Values.components.llmserver.tag }}
{{- else -}}
{{ .Values.components.llmserver.image }}:{{ .Values.components.llmserver.tag }}
{{- end }}
{{- end }}

